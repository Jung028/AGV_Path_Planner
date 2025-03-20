import pygame
import heapq
import json
import time

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS
WHITE, BLACK, BLUE, GREEN, RED = (255, 255, 255), (0, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0)

# Default Maze Representation (0 = open path, 1 = wall)
MAZE = [[0 for _ in range(COLS)] for _ in range(ROWS)]
START, END = None, None

# Dijkstra Algorithm
def dijkstra(start, end):
    heap = [(0, start)]  # (cost, position)
    distances = {start: 0}
    parents = {start: None}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while heap:
        cost, current = heapq.heappop(heap)
        if current == end:
            break
        
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and MAZE[neighbor[0]][neighbor[1]] == 0:
                new_cost = cost + 1
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    parents[neighbor] = current
                    heapq.heappush(heap, (new_cost, neighbor))
    
    path = []
    node = end
    while node:
        path.append(node)
        node = parents.get(node)
    return path[::-1] if path and path[-1] == start else []

# Save Map to File
def save_map():
    data = {"maze": MAZE, "start": START, "end": END}
    with open("map.json", "w") as f:
        json.dump(data, f)
    print("Map saved!")

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra Maze Solver")
clock = pygame.time.Clock()

def draw_grid():
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

def animate_path(path):
    for p in path:
        pygame.draw.rect(screen, BLUE, (p[1] * CELL_SIZE, p[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(200)  # Delay to show movement

driving = True
mode = 'wall'  # Default mode
while driving:
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            driving = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                mode = 'start'
            elif event.key == pygame.K_e:
                mode = 'end'
            elif event.key == pygame.K_w:
                mode = 'wall'
            elif event.key == pygame.K_f:
                save_map()
            elif event.key == pygame.K_SPACE and START and END:
                path = dijkstra(START, END)
                animate_path(path)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos(), mode)

pygame.quit()
