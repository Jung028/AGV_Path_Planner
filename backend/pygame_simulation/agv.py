from config import BLACK, RED, GRID_SIZE
import pygame

class AGV:
    def __init__(self, x, y):
        self.position = [x, y]
        self.target = None
        self.selected = False

    def draw(self, screen):
        color = RED if self.selected else BLACK  # Highlight AGV when selected
        pygame.draw.rect(screen, color, 
                         (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def move(self):
        if self.target:
            if self.position[0] < self.target[0]:
                self.position[0] += 1
            elif self.position[0] > self.target[0]:
                self.position[0] -= 1
            elif self.position[1] < self.target[1]:
                self.position[1] += 1
            elif self.position[1] > self.target[1]:
                self.position[1] -= 1
            
            if self.position == self.target:
                self.target = None

    def handle_click(self, x, y):
        """Handles click events to select AGV or set target position."""
        grid_x, grid_y = x // GRID_SIZE, y // GRID_SIZE
        if self.position == [grid_x, grid_y]:  # Clicked on AGV
            self.selected = not self.selected
        elif self.selected:  # Clicked on a destination while AGV is selected
            self.target = [grid_x, grid_y]
            self.selected = False  # Deselect AGV after selecting target
