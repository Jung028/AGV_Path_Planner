# grid.py
from config import BLUE, GRAY, GREEN, HIGHLIGHT_COLOR, RED, SCREEN_HEIGHT, SCREEN_WIDTH, YELLOW
import pygame


class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.data = {}
        self.selected_cell = None
        self.dropdown_options = ["Turning", "Idle", "Normal", "Charging"]
    
    def draw_dropdown(self, screen):
        if self.selected_cell:
            x, y = self.selected_cell[0] * self.cell_size, self.selected_cell[1] * self.cell_size
            dropdown_width = self.cell_size * 4
            dropdown_height = self.cell_size

            for i, option in enumerate(self.dropdown_options):
                option_rect = pygame.Rect(x + self.cell_size, y + (i * self.cell_size), dropdown_width, dropdown_height)
                pygame.draw.rect(screen, (220, 220, 220), option_rect)  # Light gray background
                pygame.draw.rect(screen, (0, 0, 0), option_rect, 1)  # Black border
                text = pygame.font.Font(None, 24).render(option, True, (0, 0, 0))
                screen.blit(text, (x + self.cell_size + 5, y + (i * self.cell_size) + 5))

    def draw(self, screen):
        for x in range(0, SCREEN_WIDTH, self.cell_size):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, self.cell_size):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        
        for pos, cell_type in self.data.items():
            color = GRAY
            if cell_type == "Turning":
                color = BLUE
            elif cell_type == "Charging":
                color = RED
            elif cell_type == "Idle":
                color = YELLOW
            elif cell_type == "Normal":
                color = GREEN
            pygame.draw.rect(screen, color, (pos[0] * self.cell_size, pos[1] * self.cell_size, self.cell_size, self.cell_size))
        
        if self.selected_cell:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (self.selected_cell[0] * self.cell_size, self.selected_cell[1] * self.cell_size, self.cell_size, self.cell_size))
            self.draw_dropdown(screen)
