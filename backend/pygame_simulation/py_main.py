from algorithm.dijkstra import dijkstras
from algorithm.aco import aco
from algorithm.astar import astar
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

CYAN = (0, 255, 255)         # Picking Station
DARK_ORANGE = (255, 140, 0)  # Putaway Station
DARK_PURPLE = (48, 25, 52)   # Shelf



MAPS_DIR = "maps"
current_map_name = None  # Store the map name after first input

if not os.path.exists(MAPS_DIR):
    os.makedirs(MAPS_DIR)

# Load Maps
def load_maps():
    return [f for f in os.listdir(MAPS_DIR) if f.endswith(".json")]

def generate_default_name():
    """Generates a default map name using a timestamp"""
    return f"map_{int(time.time())}"  # Example: map_1713056778

def save_map(maze, robot, end, rename=False):
    global current_map_name

    # If renaming, ask for a new name
    if rename:
        new_name = input("Enter new map name: ").strip()
        if new_name:
            current_map_name = new_name  # Update the map name

    # If it's the first time saving, generate a default name
    if current_map_name is None:
        current_map_name = generate_default_name()

    # Save the map with the current name
    data = {"maze": maze, "robot": robot, "end": end}
    file_path = os.path.join(MAPS_DIR, f"{current_map_name}.json")

    with open(file_path, "w") as f:
        json.dump(data, f)

    print(f"Map '{current_map_name}' saved successfully!")

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
            
            robot_data = data.get("robot", (0, 0))  # Get "robot" or default (0,0)
            
            if robot_data is None:  # Handle None case
                robot_data = (0, 0)

            ROBOT = tuple(robot_data)  # Ensure it's a tuple

            
            end_data = data.get("end", (ROWS-1, COLS-1))  # Get "end" or default

            if end_data is None:  # Handle None case
                end_data = (ROWS-1, COLS-1)

            END = tuple(end_data)  # Ensure it's a tuple
    

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dijkstra Robot Simulation")



    robot_path = []  # Store the robot's path
    SHELVES = []  # ✅ Store multiple shelves

    SHELF = None  # Store the shelf's position (Initially None)
    def handle_click(pos, mode):
        global ROBOT, END
        row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
        if mode == 'wall':
            MAZE[row][col] = 1 - MAZE[row][col]
        elif mode == 'robot':
            ROBOT = (row, col)
        elif mode == 'end':
            END = (row, col)
        elif mode == 'picking_station':
            MAZE[row][col] = 2  # Picking Station
        elif mode == 'putaway_station':
            MAZE[row][col] = 3  # Putaway Station
        elif mode == 'shelf':
            SHELF = (row, col)  # Shelf



    def draw_grid(robot_pos=None):
        screen.fill(WHITE)
        
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if MAZE[row][col] == 1:
                    pygame.draw.rect(screen, BLACK, rect)  # Walls
                elif MAZE[row][col] == 2:
                    pygame.draw.rect(screen, CYAN, rect)  # Picking Station
                elif MAZE[row][col] == 3:
                    pygame.draw.rect(screen, DARK_ORANGE, rect)  # Putaway Station

                pygame.draw.rect(screen, WHITE, rect, 1)  # Grid lines

        if END:
            pygame.draw.rect(screen, RED, (END[1] * CELL_SIZE, END[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if ROBOT:
            pygame.draw.rect(screen, PURPLE, (ROBOT[1] * CELL_SIZE, ROBOT[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        if SHELF:
            pygame.draw.rect(screen, DARK_PURPLE, (SHELF[1] * CELL_SIZE, SHELF[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Draw shelf

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


    def find_position(value):
        """Finds the first occurrence of a specific value in the grid."""
        for row in range(ROWS):
            for col in range(COLS):
                if MAZE[row][col] == value:
                    return (row, col)
        return None  # If not found

    shelf_pos = find_position(4)  # Locate shelf
    station_pos = find_position(2) or find_position(3)  # Picking or putaway station

    if shelf_pos and station_pos:
        original_shelf_pos = shelf_pos  # Store shelf's original position


    def move_robot():
        global ROBOT, MAZE
        
        shelf_pos = find_position(4)  # Locate shelf
        station_pos = find_position(2) or find_position(3)  # Find either picking or putaway station
        
        if not shelf_pos or not station_pos:
            print("Shelf or Station not found!")
            return
        
        original_shelf_pos = shelf_pos  # Store shelf's original position
        
        # 1. Move to Shelf
        path_to_shelf = astar(MAZE, ROBOT, shelf_pos)
        if path_to_shelf:
            follow_path(path_to_shelf)

        # 2. Pick up Shelf (Remove from Grid)
        MAZE[shelf_pos[0]][shelf_pos[1]] = 0  

        # 3. Move to Putaway/Picking Station
        path_to_station = astar(MAZE, shelf_pos, station_pos)
        if path_to_station:
            follow_path(path_to_station)

        # 4. Wait for 3 seconds
        time.sleep(3)

        # 5. Move back to the original shelf position
        path_back = astar(MAZE, station_pos, original_shelf_pos)
        if path_back:
            follow_path(path_back)

        # 6. Place Shelf Back
        MAZE[original_shelf_pos[0]][original_shelf_pos[1]] = 4  


    def follow_path(path):
        global ROBOT
        for step in path:
            ROBOT = step  # Move robot
            draw_grid(ROBOT)  # Redraw grid to show movement
            pygame.time.delay(500)  # Delay for animation


  
     
    

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
                elif event.key == pygame.K_p:
                    mode = 'picking_station'  # Press 'P' for Picking Station
                elif event.key == pygame.K_t:
                    mode = 'putaway_station'  # Press 'T' for Putaway Station
                elif event.key == pygame.K_g:
                    mode = 'shelf'  # Press 'P' to place a shelf
                elif event.key == pygame.K_SPACE:
                    if ROBOT is None or END is None:
                        print("Error: Place both the robot and the end position before running Dijkstra.")
                    else:
                        path = aco(MAZE ,ROBOT, END)  # Now we are sure both are set
                        animate_robot(screen, path)
                
                elif event.key == pygame.K_f:
                    save_map(MAZE, ROBOT, END)

                elif event.key == pygame.K_q:
                    save_map(MAZE, ROBOT, END, rename=True)  # Rename and save
                
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
                    robot_path.clear()  # ✅ Clear previous path to remove cyan color

                    draw_grid(ROBOT)  # ✅ Fix: Update immediately after placing the robot
                elif mode == 'end':
                    END = (row, col)
                elif mode == 'picking_station':
                    MAZE[row][col] = 2  # Assign picking station (new representation)
                elif mode == 'putaway_station':
                    MAZE[row][col] = 3  # Assign putaway station
                elif mode == 'shelf':
                    if (row, col) not in SHELVES:  # ✅ Avoid duplicate shelves
                        SHELVES.append((row, col))  # ✅ Add new shelf instead of replacing
                    draw_grid(ROBOT)  # ✅ Redraw grid to reflect changes
                    
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
