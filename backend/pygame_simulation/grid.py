import pygame

class Grid:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen, cell_size):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Black grid lines
