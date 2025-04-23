# author: Yeifer Ronaldo Muñoz Valencia
# greedy.py

import heapq
from agent.SearchAlgorithm import SearchAlgorithm

class Greedy(SearchAlgorithm):
    def __init__(self, grid):
        self.grid = grid
        self.visited = set()

    def heuristic(self, a, b):
        # heurística de Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (self.heuristic(start, goal), start, [start]))  # (heurística, posición, camino)
        self.visited.clear()

        while open_list:
            h_current, current_pos, path = heapq.heappop(open_list)

            if current_pos == goal:
                return path

            if current_pos in self.visited:
                continue
            self.visited.add(current_pos)

            # Pintar la celda actual de violeta
            cell = self.grid.get_cell(current_pos)
            cell.make_traversed((148, 0, 211))  # violeta

            for neighbor in self.grid.get_neighbors(current_pos):
                if neighbor not in self.visited:
                    h_neighbor = self.heuristic(neighbor, goal)
                    new_path = path + [neighbor]
                    heapq.heappush(open_list, (h_neighbor, neighbor, new_path))

        return None
