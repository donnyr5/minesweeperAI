import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def show_cells(self):
        return self.cells

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if (self.count == len(self.cells)):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if (self.count == 0 ):
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if (self.cells.__contains__(cell)):
            self.cells.remove(cell)
            self.count = self.count - 1 #remove and decrement count because a mine is gone

        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if (self.cells.__contains__(cell)):
            self.cells.remove(cell)
            #remove but leave the count because we arent removing a mine.

        return

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        #keep track of unclicked squares
        self.unclicked = []
        for i in range(self.height):
            for j in range(self.width):
                    self.unclicked.append((i,j))

     
        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
            based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
            if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
            if they can be inferred from existing knowledge
        """
        # print("clicked: ", cell)
        self.moves_made.add(cell)
        self.mark_safe(cell)
        self.unclicked.remove(cell)  # we have clicked the cell

        # Calculate bounds for neighbors 
        lower_bound_x = max(0, cell[0] - 1)
        upper_bound_x = min(self.width, cell[0] + 2)
        lower_bound_y = max(0, cell[1] - 1)
        upper_bound_y = min(self.height, cell[1] + 2)

        # Based on the cell's location, create a sentence with all unclicked neighbors and the count
        unclicked_neighbors = [(i, j) 
                            for i in range(lower_bound_x, upper_bound_x) 
                            for j in range(lower_bound_y, upper_bound_y) 
                            if (i, j) not in self.moves_made]
        
        self.knowledge.append(Sentence(unclicked_neighbors, count))

        self.make_inferences()
        self.check_obvious()

        # We have likely identified a safe move, but if not, we will try again
        if len(self.safes) == 0:
            self.make_inferences()
            self.check_obvious()

        # print("known safes: ", self.safes - self.moves_made)
        # print("known mines: ", self.mines)

    def check_obvious(self):
        # We need to check all sentences to see if there are any obvious mines or safe spots.

        empty_sets = []  # List of sentences
        safe_cells = []
        mine_cells = []

        for sentence in self.knowledge:
            # skip empty sets
            if len(sentence.show_cells()) == 0:
                empty_sets.append(sentence)
                continue

            if sentence.known_safes() is not None:
                for element in sentence.known_safes():
                    safe_cells.append(element)

            if sentence.known_mines() is not None:
                for element in sentence.known_mines():
                    mine_cells.append(element)

        # Remove empty sets from the knowledge base
        for element in empty_sets:
            self.knowledge.remove(element)

        for element in safe_cells:
            self.mark_safe(element)

        for element in mine_cells:
            self.mark_mine(element)

        return


    def make_inferences(self):
            #this is order n^2 idk how to make it less.
            #update new knowledge based on subset idea
            new_knowledge = []

            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1.cells < sentence2.cells:
                        new_knowledge.append(Sentence(sentence2.cells - sentence1.cells, sentence2.count - sentence1.count))
    
            # Create new sentences from the new_knowledge list elements and add them to self.knowledge
            for new_sentence in new_knowledge:
                if self.knowledge.__contains__(new_sentence):
                    continue
                self.knowledge.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_cells_list = list(self.safes - self.moves_made)  # Convert the set to a list

        if (len(safe_cells_list) > 0):
            candidate = random.choice(safe_cells_list)
            return candidate
        
        return None
                


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        mines_list = list(self.mines)
        options = [x for x in self.unclicked if x not in mines_list]

        if len(options) > 0:
            candidate = random.choice(options)      #random unclicked, non-mine, square
            return candidate     #it wil be removed when clicked. 
            
        return None



        
