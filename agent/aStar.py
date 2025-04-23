import heapq
import pygame
from agent.SearchAlgorithm import SearchAlgorithm

class AStar(SearchAlgorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self.explored_cells = []  # <- Guardar las celdas que explora

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))

    def find_path(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (self.heuristic(start, goal), start))
        g_cost = {start: 0}
        came_from = {}
        closed_set = set()
        self.explored_cells.clear()

        while open_list:
            f_current, current = heapq.heappop(open_list)

            if current in closed_set:
                continue
            closed_set.add(current)

            # Guardar la celda como explorada
            self.explored_cells.append(current)

            # Pintar celda recorrida (dorada para A*)
            cell = self.grid.get_cell(current)
            if current != start and current != goal:
                cell.make_traversed((255, 215, 0))  # Dorado para A*
                pygame.display.update()
                pygame.time.delay(20)

            if current == goal:
                self.final_cost = g_cost[current]
                return self.reconstruct_path(came_from, current)

            if getattr(self.grid, 'changed', False):
                return None

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current):
                tentative_g = g_cost[current] + move_cost

                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    came_from[neighbor] = current
                    g_cost[neighbor] = tentative_g
                    f_cost = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, neighbor))

        # Si no hay camino, simplemente retorna None (las celdas exploradas ya fueron guardadas)
        return None
