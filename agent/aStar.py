import heapq
import pygame
from agent.SearchAlgorithm import SearchAlgorithm

class AStar(SearchAlgorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self.final_cost = 0
        self.explored_cells = [] 

    def heuristic(self, a, b):
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        base_h = dx + dy
        penalty = 0
        search_radius = 2

        step_x = 1 if b[0] > a[0] else -1 if b[0] < a[0] else 0
        step_y = 1 if b[1] > a[1] else -1 if b[1] < a[1] else 0

        for i in range(-search_radius, search_radius + 1):
            for j in range(-search_radius, search_radius + 1):
                x_coord = a[0] + i * step_x
                y_coord = a[1] + j * step_y

                if 0 <= x_coord < self.grid.rows and 0 <= y_coord < self.grid.columns:
                    cell = self.grid.get_cell((x_coord, y_coord))  # Tupla como argumento
                    if cell.cost > 1:
                        distance = (i**2 + j**2)**0.5
                        penalty += (cell.cost * 0.15) / (distance + 1)

        return base_h + penalty


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
            if current == goal:
                self.final_cost = g_cost[current]
                return self.reconstruct_path(came_from, current)
            if current in closed_set:
                continue
            closed_set.add(current)
            self.explored_cells.append(current)

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

        return None

