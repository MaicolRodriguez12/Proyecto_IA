# ucs.py
from .SearchAlgorithm import SearchAlgorithm
import heapq

class UCS(SearchAlgorithm):
    def __init__(self, grid):
        self.grid = grid
        self.final_cost = 0  # Para mostrar el costo final en la UI (si aplica)

    def find_path(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start))
        g_cost = {start: 0}
        came_from = {}
        visited = set()

        while open_list:
            cost, current = heapq.heappop(open_list)

            if current in visited:
                continue
            visited.add(current)

            cell = self.grid.get_cell(current)
            cell.make_traversed((255, 105, 180)) 

            if current == goal:
                path = [goal]
                while path[-1] in came_from:
                    path.append(came_from[path[-1]])
                self.final_cost = cost
                return list(reversed(path))

            for neigh in self.grid.get_neighbors(current):
                cell = self.grid.get_cell(neigh)
                new_cost = g_cost[current] + cell.cost
                if neigh not in g_cost or new_cost < g_cost[neigh]:
                    g_cost[neigh] = new_cost
                    came_from[neigh] = current
                    heapq.heappush(open_list, (new_cost, neigh))

        return None
