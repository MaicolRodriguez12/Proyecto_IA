import heapq
import pygame
from agent.SearchAlgorithm import SearchAlgorithm

class AStar(SearchAlgorithm):
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

        while open_list:
            f_current, current = heapq.heappop(open_list)

            # Pintar la celda actual mientras se recorre
            cell = self.grid.get_cell(current)
            if current != start and current != goal:
                cell.make_traversed((255, 215, 0))  # Dorado para A*
                pygame.display.update()
                pygame.time.delay(20)

            if current == goal:
                self.final_cost = g_cost[current]
                return self.reconstruct_path(came_from, current)
            if current in closed_set:
                continue
            closed_set.add(current)

            if getattr(self.grid, 'changed', False):
                return None

            for neighbor in self.get_neighbors(current):
                cell = self.grid.get_cell(neighbor)
                if cell.is_wall('top'):
                    pass
                tentative_g = g_cost[current] + cell.cost

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current):
                tentative_g = g_cost[current] + move_cost

                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    came_from[neighbor] = current
                    g_cost[neighbor] = tentative_g
                    f_cost = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, neighbor))
            
        return None

