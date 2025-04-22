# author: Yeifer Ronaldo Muñoz Valencia

import heapq
from laberinto.grid import Grid

class Greedy:
    def __init__(self, grid):
        self.grid = grid

    def heuristic(self, a, b):
        # heuristica de Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (self.heuristic(start, goal), start, [start]))  # (heurística, posición, camino)
        visited = set()

        while open_list:
            h_current, current_pos, path = heapq.heappop(open_list)

            if current_pos == goal:
                return path

            if current_pos in visited:
                continue
            visited.add(current_pos)

            for neighbor in self.grid.get_neighbors(current_pos):
                if neighbor not in visited:
                    h_neighbor = self.heuristic(neighbor, goal)
                    new_path = path + [neighbor]
                    heapq.heappush(open_list, (h_neighbor, neighbor, new_path))

        return None  