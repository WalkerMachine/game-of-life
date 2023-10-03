# Conway's Game of Life

Conway's Game of Life is a cellular automaton devised by mathematician John Conway. It's a classic example of a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. This Python program uses the Pygame library to simulate Conway's Game of Life.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame (install using `pip install pygame`)

### Running the Program

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt.

3. Navigate to the project directory.

4. Run the following command to start the simulation: python3 main.py

5. Follow the on-screen instructions to interact with the simulation.

## How to Play

- **Left-click**: Toggle cell state (alive/dead) at the clicked position.
- **Spacebar**: Pause/unpause the simulation.
- **C**: Clear the grid.
- **N**: Generate a random pattern on the grid.

## Rules

In Conway's Game of Life, each cell can be in one of two states: alive or dead. The game operates based on the following rules:

1. A live cell with 2 or 3 live neighbors survives to the next generation.
2. A dead cell with exactly 3 live neighbors becomes a live cell.
3. All other live cells die in the next generation, and all other dead cells remain dead.

The game continues to evolve generation by generation, creating various patterns and behaviors.

## Features

- Interactive grid that allows you to create and experiment with different patterns.
- Pause and resume the simulation to observe specific states.
- Clear the grid to start fresh or generate random patterns.

## Author

- [Zvonimir Stipanovic]

## Acknowledgments

- This program is inspired by John Conway's Game of Life and various Python and Pygame tutorials available online.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/WalkerMachine/game-of-life/blob/main/LICENSE.txt) file for details.

---

Enjoy exploring the fascinating world of cellular automata with Conway's Game of Life!
