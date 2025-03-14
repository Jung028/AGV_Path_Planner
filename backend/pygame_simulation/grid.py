# grid.py
from config import BLUE, DROPDOWN_BG, DROPDOWN_BORDER, GRAY, GREEN, HIGHLIGHT_COLOR, RED, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, YELLOW
import pygame


class Grid:
    def __init__(self):
        self.data = {}  # Store placed points with exact screen coordinates
        self.selected_point = None  # Store selected position as exact screen coordinates
        self.dropdown_options = ["Turning", "Idle", "Normal", "Charging"]
        self.dropdown_active = False  # Track if dropdown should be visible

    def draw_dropdown(self, screen):
        if self.selected_point:
            x, y = self.selected_point  # Use exact screen coordinates
            dropdown_width = 120  # Fixed width for dropdown
            dropdown_height = 30  # Fixed height for each option

            for i, option in enumerate(self.dropdown_options):
                option_rect = pygame.Rect(x + 10, y + (i * dropdown_height), dropdown_width, dropdown_height)
                pygame.draw.rect(screen, DROPDOWN_BG, option_rect)  # Background color
                pygame.draw.rect(screen, DROPDOWN_BORDER, option_rect, 2)  # Border color
                text = pygame.font.Font(None, 24).render(option, True, (0, 0, 0))
                screen.blit(text, (x + 15, y + (i * dropdown_height) + 5))

    def draw(self, screen):
        screen.fill(WHITE)  # Clear screen with a plain white background

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
            pygame.draw.circle(screen, color, pos, 8)  # Represent points as circles
        
        if self.dropdown_active and self.selected_point:
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, self.selected_point, 10)  # Highlight selection
            self.draw_dropdown(screen)
