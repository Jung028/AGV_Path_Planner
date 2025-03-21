
# Dijkstra's Algorithm
import heapq


def dijkstras(maze, robot, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    pq = [(0, robot)]
    distances = {robot: 0}
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
