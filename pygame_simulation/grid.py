import pygame

# Constants
GRID_SIZE = 20  # Number of cells per row/column
CELL_SIZE = 30  # Size of each cell in pixels
SCREEN_SIZE = GRID_SIZE * CELL_SIZE  # Total screen size

class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # 0 = empty cell

    def draw(self, screen):
        """Draw the grid lines."""
        for x in range(0, SCREEN_SIZE, CELL_SIZE):
            for y in range(0, SCREEN_SIZE, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    def place_object(self, x, y, value):
        """Places an object in the grid (1 = obstacle, 2 = charging station, 3 = robot)."""
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            self.grid[y][x] = value  # Store the object in the grid

    def get_grid(self):
        return self.grid
