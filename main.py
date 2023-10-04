import pygame
from game import GameOfLife, Settings


# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
FPS = 120

# Create a GameOfLife instance
game = GameOfLife(WIDTH, HEIGHT, TILE_SIZE, FPS)

if __name__ == '__main__':
    game.run()
     