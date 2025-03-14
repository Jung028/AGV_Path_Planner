# game.py
from config import *
from grid import Grid
from agv import AGV

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AGV Path Planner")
        self.clock = pygame.time.Clock()
        self.grid = Grid()
        self.agv = AGV(5, 5)
        self.running = True
    
    def run(self):
        while self.running:
            self.screen.fill(WHITE)
            self.grid.draw(self.screen)
            self.agv.move()
            self.agv.draw(self.screen)
            
            for event in pygame.event.get():
                self.handle_event(event)
            
            pygame.display.flip()
            self.clock.tick(10)
        
        pygame.quit()
        sys.exit()
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.grid.dropdown_active:
                for i, option in enumerate(self.grid.dropdown_options):
                    option_rect = pygame.Rect(self.grid.selected_point[0] + 10, 
                                            self.grid.selected_point[1] + (i * 30), 
                                            120, 30)
                    if option_rect.collidepoint(x, y):
                        self.grid.data[self.grid.selected_point] = option
                        self.grid.dropdown_active = False
                        self.grid.selected_point = None
                        break
            else:
                self.grid.selected_point = (x, y)  # Set selected point anywhere on the map
                self.grid.dropdown_active = True   # Activate dropdown visibility

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.agv.target:
                self.agv.move()
