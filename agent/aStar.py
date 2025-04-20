#author: Yeifer Ronaldo Muñoz Valencia

from .SearchAlgorithm import SearchAlgorithm
import heapq

# Implementación de búsqueda A*
class AStar(SearchAlgorithm):
    def heuristic(self, a, b):
        #Heuristica Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start, [start]))  # (f_cost, posición, camino)
        g_cost = {start: 0}  # Costo acumulado

        while open_list:
            f_current, current_pos, path = heapq.heappop(open_list)

            if current_pos == goal:
                return path

            for neighbor in self.get_neighbors(current_pos):
                cell = self.grid.cells[neighbor[0]][neighbor[1]]
                if cell.is_wall:
                    continue

                tentative_g = g_cost[current_pos] + cell.cost  # Costo acumulado + costo de la celda
                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g
                    f_cost = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, neighbor, path + [neighbor]))

        return None