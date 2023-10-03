import pygame
from game import GameOfLife


# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
FPS = 60

# Create a GameOfLife instance
game = GameOfLife(WIDTH, HEIGHT, TILE_SIZE, FPS)

if __name__ == '__main__':
    game.run()
     