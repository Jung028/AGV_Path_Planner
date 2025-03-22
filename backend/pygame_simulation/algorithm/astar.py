import heapq

def heuristic(a, b):
    """Calculate the Manhattan distance heuristic between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    """Find the shortest path from start to goal using A* algorithm."""
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))  # Priority Queue with (cost, position)
    
    came_from = {}  # Store path history
    g_score = {node: float('inf') for row in grid for node in enumerate(row)}
    g_score[start] = 0
    f_score = {node: float('inf') for row in grid for node in enumerate(row)}
    f_score[start] = heuristic(start, goal)
    
    while open_set:
        _, current = heapq.heappop(open_set)  # Get the node with the lowest cost
        
        if current == goal:  # Reached the goal
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path  # Return reconstructed path
        
        # Explore Neighbors (Up, Down, Left, Right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:  # Stay inside grid
                if grid[neighbor[0]][neighbor[1]] == 1:  # Obstacle check
                    continue
                
                temp_g_score = g_score[current] + 1  # Cost from start
                
                if temp_g_score < g_score[neighbor]:  # Better path found
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None  # No path found
