from algorithm.dijkstra import dijkstras
from algorithm.aco import aco
import pygame # type: ignore
import heapq
import json
import os
import time

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 40, 40
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 128)

LIGHT_BLUE = (173, 216, 230)  # Soft blue for the trail
ORANGE = (255, 165, 0)  # Orange for the previous position



MAPS_DIR = "maps"
if not os.path.exists(MAPS_DIR):
    os.makedirs(MAPS_DIR)

# Load Maps
def load_maps():
    return [f for f in os.listdir(MAPS_DIR) if f.endswith(".json")]

# Save Map to File
def save_map(map_name, maze, robot, end):
    data = {"maze": maze, "robot": robot, "end": end}
    with open(os.path.join(MAPS_DIR, f"{map_name}.json"), "w") as f:
        json.dump(data, f)
    print("Map saved!")


# Map Editor
def edit_map(map_name):
    global MAZE, ROBOT, END
    if map_name == "new_map":
        MAZE = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        ROBOT, END = None, None
    else:
        with open(os.path.join(MAPS_DIR, f"{map_name}.json"), "r") as f:
            data = json.load(f)
            MAZE = data["maze"]
            ROBOT = tuple(data.get("robot", (0, 0)))  # Default to (0,0) if missing
            END = tuple(data.get("end", (ROWS-1, COLS-1)))  # Default to bottom-right
    

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dijkstra Robot Simulation")



    robot_path = []  # Store the robot's path

    def draw_grid(robot_pos=None):
        screen.fill(WHITE)
        
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if MAZE[row][col] == 1:
                    pygame.draw.rect(screen, BLACK, rect)  # Walls
                
                pygame.draw.rect(screen, WHITE, rect, 1)  # Grid lines

        if END:
            pygame.draw.rect(screen, RED, (END[1] * CELL_SIZE, END[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if ROBOT:
            pygame.draw.rect(screen, PURPLE, (ROBOT[1] * CELL_SIZE, ROBOT[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the robot's path
        for pos in robot_path:
            pygame.draw.rect(screen, LIGHT_BLUE, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Trail color

        if robot_path:  
            last_pos = robot_path[-1]  # Last visited position
            pygame.draw.rect(screen, ORANGE, (last_pos[1] * CELL_SIZE, last_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Mark last position

        if robot_pos:
            robot_path.append(robot_pos)  # Add current position to path
            pygame.draw.rect(screen, PURPLE, (robot_pos[1] * CELL_SIZE, robot_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Draw robot

        pygame.display.flip()


    # Animate Robot Movement
    def animate_robot(screen, path):
        """ Animate the robot moving along the path. """
        for pos in path:
            draw_grid(pos)
            pygame.time.delay(200)  # Slow down animation
        print("Robot reached the end!")
        
    def handle_click(pos, mode):
        global ROBOT, END
        row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
        if mode == 'wall':
            MAZE[row][col] = 1 - MAZE[row][col]
        elif mode == 'robot':
            ROBOT = (row, col)
        elif mode == 'end':
            END = (row, col)
        draw_grid()

    draw_grid()
    mode = 'wall'  # Default mode
    running = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mode = 'robot'
                elif event.key == pygame.K_e:
                    mode = 'end'
                elif event.key == pygame.K_w:
                    mode = 'wall'
                elif event.key == pygame.K_SPACE:
                    if ROBOT is None or END is None:
                        print("Error: Place both the robot and the end position before running Dijkstra.")
                    else:
                        path = aco(MAZE ,ROBOT, END)  # Now we are sure both are set
                        animate_robot(screen, path)
                elif event.key == pygame.K_f:
                    save_map(map_name, MAZE, ROBOT, END)
                elif event.key == pygame.K_m:
                    running = False
                    main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if mode == 'wall':
                    MAZE[row][col] = 1 - MAZE[row][col]
                elif mode == 'robot':
                    ROBOT = (row, col)
                    draw_grid(ROBOT)  # ✅ Fix: Update immediately after placing the robot
                elif mode == 'end':
                    END = (row, col)
                draw_grid(ROBOT)  # ✅ Ensure grid updates after changes

    pygame.quit()


# Main Menu
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Map Selector")
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        screen.fill(WHITE)
        maps = load_maps()
        y_offset = 50
        for i, map_name in enumerate(maps):
            text_surface = font.render(map_name, True, BLACK)
            screen.blit(text_surface, (50, y_offset + i * 40))

        create_text = font.render("+ Create New Map", True, GREEN)
        screen.blit(create_text, (50, y_offset + len(maps) * 40 + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y > y_offset + len(maps) * 40:  # Clicked on "Create New Map"
                    edit_map("new_map")
                else:
                    index = (y - y_offset) // 40
                    if 0 <= index < len(maps):
                        edit_map(maps[index].replace(".json", ""))

    pygame.quit()

if __name__ == "__main__":
    main_menu()
