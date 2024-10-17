# AI Minesweeper Solver

## Overview
Created an AI that can play Minesweeper, a classic puzzle game. The game consists of a grid of cells, some containing hidden mines. The AI must use logical deduction to flag all mines without detonating any.

## Project Description
- **Game Basics:** Minesweeper is played on a grid with hidden mines. Safe cells show the count of neighboring mines.
- **Objective:** Flag all mines. The AI will use knowledge-based decision-making to solve the puzzle.
- **AI Knowledge Representation:** Each cell is a propositional variable: true if it contains a mine, false otherwise. The AI learns from revealed safe cells.

## Knowledge Representation
AI's knowledge is represented as sentences with a set of cells and a count of how many of those cells are mines. Example: `{A, B, C, D, E, F, G, H} = 1`.

## Project Structure
1. `runner.py`: Manages the game's graphical interface.
2. `minesweeper.py`: Contains game logic and AI decision-making algorithms.

### Minesweeper.py Overview
- **Minesweeper Class:** Manages gameplay.
- **Sentence Class:** Represents logical sentences about game state. 
- **MinesweeperAI Class:** Handles AI operations, including tracking moves and updating knowledge.
