# game.py
from config import *
from grid import Grid
from agv import AGV

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AGV Path Planner")
        self.clock = pygame.time.Clock()
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT, GRID_SIZE)
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
            grid_x, grid_y = x // GRID_SIZE, y // GRID_SIZE
            
            if (grid_x, grid_y) == tuple(self.agv.position):
                self.agv.selected = True
            elif self.agv.selected:
                self.agv.target = [grid_x, grid_y]
                self.agv.selected = False
            elif self.grid.selected_cell:
                for i, option in enumerate(self.grid.dropdown_options):
                    option_rect = pygame.Rect(self.grid.selected_cell[0] * GRID_SIZE + GRID_SIZE, 
                                              self.grid.selected_cell[1] * GRID_SIZE + (i * GRID_SIZE), 
                                              GRID_SIZE * 4, GRID_SIZE)
                    if option_rect.collidepoint(x, y):
                        self.grid.data[(self.grid.selected_cell[0], self.grid.selected_cell[1])] = option
                        self.grid.selected_cell = None
                        break
            else:
                self.grid.selected_cell = (grid_x, grid_y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.agv.target:
                self.agv.move()
