from .SearchAlgorithm import SearchAlgorithm
import heapq

class AStar(SearchAlgorithm):
    def heuristic(self, a, b):
        # Heurística Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        # Reconstruye el camino desde "came_from" cuando se llega a la meta
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))

    def find_path(self, start, goal):
        open_list = []
        # (f_cost, posición)
        heapq.heappush(open_list, (self.heuristic(start, goal), start))

        g_cost = {start: 0}
        came_from = {}         
        closed_set = set()      

        while open_list:
            f_current, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            if current in closed_set:
                continue
            closed_set.add(current)

           
            if self.grid.changed:
                self.grid.changed = False
                

            # Explorar vecinos
            for neighbor in self.get_neighbors(current):
                cell = self.grid.cells[neighbor[0]][neighbor[1]]
                if cell.is_wall:
                    continue

                tentative_g = g_cost[current] + cell.cost

                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    came_from[neighbor] = current
                    g_cost[neighbor] = tentative_g
                    f_cost = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, neighbor))

        # No hay camino posible
        return None
