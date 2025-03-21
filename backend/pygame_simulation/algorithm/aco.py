# algorithm/aco.py
import numpy as np
import random

def aco(maze, start, end, num_ants=10, num_iterations=100, alpha=1.0, beta=2.0, evaporation_rate=0.5, pheromone_deposit=1.0):
    rows, cols = len(maze), len(maze[0])
    pheromone = np.ones((rows, cols))  # Initialize pheromone matrix
    best_path = None
    best_path_length = float('inf')
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    
    def is_valid_move(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0
    
    for _ in range(num_iterations):
        all_paths = []
        
        for _ in range(num_ants):
            path = [start]
            visited = set()
            visited.add(start)
            current_pos = start
            
            while current_pos != end:
                neighbors = [(current_pos[0] + dx, current_pos[1] + dy) for dx, dy in directions]
                valid_neighbors = [(x, y) for x, y in neighbors if is_valid_move(x, y) and (x, y) not in visited]
                
                if not valid_neighbors:
                    break  # Dead-end, stop exploring
                
                # Compute probabilities based on pheromone and heuristic distance
                desirability = [pheromone[x][y] ** alpha * (1.0 / (abs(x - end[0]) + abs(y - end[1]) + 1)) ** beta for x, y in valid_neighbors]
                total = sum(desirability)
                probabilities = [d / total for d in desirability]
                
                next_pos = random.choices(valid_neighbors, probabilities)[0]
                path.append(next_pos)
                visited.add(next_pos)
                current_pos = next_pos
            
            if path[-1] == end and len(path) < best_path_length:
                best_path = path
                best_path_length = len(path)
            
            all_paths.append(path)
        
        # Update pheromone matrix
        pheromone *= (1 - evaporation_rate)  # Evaporation
        for path in all_paths:
            if path[-1] == end:  # Only reinforce successful paths
                for x, y in path:
                    pheromone[x][y] += pheromone_deposit / len(path)
    
    return best_path if best_path else []
