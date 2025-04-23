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

        heapq.heappush(open_list, (self.heuristic(start, goal), 0, start, [start]))  # (heurística, costo, posición, camino)
        self.visited.clear()

        while open_list:
            h_current, cost_so_far, current_pos, path = heapq.heappop(open_list)  # Desempaquetar 4 valores

            if current_pos == goal:
                self.final_cost = cost_so_far
                return path

            if current_pos in self.visited:
                continue
            self.visited.add(current_pos)

            # Pintar la celda actual de violeta
            cell = self.grid.get_cell(current_pos)
            cell.make_traversed((148, 0, 211))  # violeta

            # Explorar los vecinos
            for neighbor in self.grid.get_neighbors(current_pos):
                if neighbor not in self.visited:
                    h_neighbor = self.heuristic(neighbor, goal)
                    new_path = path + [neighbor]
                    heapq.heappush(open_list, (h_neighbor, cost_so_far + 1, neighbor, new_path))  # Empujar 4 valores

        return None  # No hay camino
