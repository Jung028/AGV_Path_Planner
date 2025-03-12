import pygame
from grid import Grid
from robot import Robot

# Initialize Pygame
pygame.init()
SCREEN_SIZE = 600
CELL_SIZE = SCREEN_SIZE // 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Warehouse Robot Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create grid and robot
        self.grid = Grid()
        self.robot = Robot(5, 5)  # Start robot at (5,5)

        # Add test objects
        self.grid.place_object(8, 8, 1)  # Obstacle
        self.grid.place_object(10, 10, 2)  # Charging Station

    def run(self):
        """Main loop for running the simulation."""
        while self.running:
            self.screen.fill(WHITE)
            self.grid.draw(self.screen)
            self.robot.draw(self.screen, CELL_SIZE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.robot.move_to(self.robot.x + 1, self.robot.y)
                    elif event.key == pygame.K_LEFT:
                        self.robot.move_to(self.robot.x - 1, self.robot.y)
                    elif event.key == pygame.K_UP:
                        self.robot.move_to(self.robot.x, self.robot.y - 1)
                    elif event.key == pygame.K_DOWN:
                        self.robot.move_to(self.robot.x, self.robot.y + 1)

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()
