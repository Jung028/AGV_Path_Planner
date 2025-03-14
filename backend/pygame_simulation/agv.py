# agv.py

from config import BLACK, GRID_SIZE
import pygame

class AGV:
    def __init__(self, x, y):
        self.position = [x, y]
        self.target = None
        self.selected = False

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
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