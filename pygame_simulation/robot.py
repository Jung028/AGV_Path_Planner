import pygame

class Robot:
    def __init__(self, x, y, color=(0, 255, 0)):
        self.x = x  # Grid X position
        self.y = y  # Grid Y position
        self.color = color
        self.path = []  # Stores movement path

    def move_to(self, new_x, new_y):
        """Moves the robot to a new position (if valid)."""
        self.path.append((self.x, self.y))  # Store previous position
        self.x, self.y = new_x, new_y

    def draw(self, screen, cell_size):
        """Draws the robot on the screen."""
        pygame.draw.circle(screen, self.color, 
                           (self.x * cell_size + cell_size // 2, self.y * cell_size + cell_size // 2), 
                           cell_size // 3)
