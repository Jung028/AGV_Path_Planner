import pygame
import heapq
import json
import os

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 40, 40
CELL_SIZE = WIDTH // COLS
WHITE, BLACK, BLUE, GREEN, RED, YELLOW = (255, 255, 255), (0, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)

MAPS_DIR = "maps"
if not os.path.exists(MAPS_DIR):
    os.makedirs(MAPS_DIR)

# Load Maps
def load_maps():
    return [f for f in os.listdir(MAPS_DIR) if f.endswith(".json")]

# Save Map to File
def save_map(map_name, maze, start, end):
    data = {"maze": maze, "start": start, "end": end}
    with open(os.path.join(MAPS_DIR, f"{map_name}.json"), "w") as f:
        json.dump(data, f)
    print("Map saved!")

# Main Page for Selecting or Creating Maps
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

def dijkstra(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    pq = [(0, start)]
    distances = {start: 0}
    predecessors = {}

    while pq:
        cost, current = heapq.heappop(pq)
        if current == end:
            path = []
            while current in predecessors:
                path.append(current)
                current = predecessors[current]
            path.reverse()
            return path  # Return shortest path

        for d in directions:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                new_cost = cost + 1
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor))
                    predecessors[neighbor] = current

    return []  # No path found

def edit_map(map_name):
    global MAZE, START, END
    if map_name == "new_map":
        MAZE = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        START, END = None, None
    else:
        with open(os.path.join(MAPS_DIR, f"{map_name}.json"), "r") as f:
            data = json.load(f)
            MAZE = data["maze"]
            START, END = tuple(data["start"]), tuple(data["end"])

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dijkstra Maze Solver")

    def draw_grid(path=None):
        screen.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if MAZE[row][col] == 1:
                    pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)
        
        if START:
            pygame.draw.rect(screen, GREEN, (START[1] * CELL_SIZE, START[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if END:
            pygame.draw.rect(screen, RED, (END[1] * CELL_SIZE, END[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if path:
            for row, col in path:
                pygame.draw.rect(screen, YELLOW, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

    def handle_click(pos, mode):
        global START, END
        row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
        if mode == 'wall':
            MAZE[row][col] = 1 - MAZE[row][col]
        elif mode == 'start':
            START = (row, col)
        elif mode == 'end':
            END = (row, col)
        draw_grid()

    draw_grid()
    mode = 'wall'  # Default mode
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    mode = 'start'
                elif event.key == pygame.K_e:
                    mode = 'end'
                elif event.key == pygame.K_w:
                    mode = 'wall'
                elif event.key == pygame.K_f:
                    save_map(map_name, MAZE, START, END)
                elif event.key == pygame.K_m:
                    running = False
                    main_menu()
                elif event.key == pygame.K_SPACE and START and END:
                    path = dijkstra(MAZE, START, END)
                    draw_grid(path)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(pygame.mouse.get_pos(), mode)

    pygame.quit()

if __name__ == "__main__":
    main_menu()
