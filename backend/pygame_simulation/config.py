# config.py
import pygame

# Grid Settings
GRID_SIZE = 20  # Size of each grid cell
GRID_WIDTH = 40  # Grid width (cells)
GRID_HEIGHT = 30  # Grid height (cells)
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (220, 220, 220)
HIGHLIGHT_COLOR = (173, 216, 230)

# Initialize pygame
pygame.init()