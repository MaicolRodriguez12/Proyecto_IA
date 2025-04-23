import heapq
from agent.SearchAlgorithm import SearchAlgorithm

class Greedy(SearchAlgorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self.explored_cells = []  # Celdas exploradas

    def heuristic(self, a, b):
        # Heurística de Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (self.heuristic(start, goal), 0, start, [start]))  # (heurística, costo, posición, camino)
        self.visited.clear()
        self.explored_cells.clear()

        while open_list:
            h_current, cost_so_far, current_pos, path = heapq.heappop(open_list)

            if current_pos == goal:
                self.final_cost = cost_so_far
                return path

            if current_pos in self.visited:
                continue
            self.visited.add(current_pos)

            # Pintar y guardar celda como explorada
            cell = self.grid.get_cell(current_pos)
            cell.make_traversed((148, 0, 211))  # Violeta para Greedy
            self.explored_cells.append(current_pos)

            # Explorar vecinos
            for neighbor in self.grid.get_neighbors(current_pos):
                if neighbor not in self.visited:
                    h_neighbor = self.heuristic(neighbor, goal)
                    new_path = path + [neighbor]
                    heapq.heappush(open_list, (h_neighbor, cost_so_far + 1, neighbor, new_path))

        return None  # No hay camino
