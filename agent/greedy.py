import heapq
from agent.SearchAlgorithm import SearchAlgorithm

class Greedy(SearchAlgorithm):
    def __init__(self, grid):
        self.grid = grid

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (self.heuristic(start, goal), 0, start, [start]))  # (heurística, costo, posición, camino)
        visited = set()

        while open_list:
            h_current, cost_so_far, current_pos, path = heapq.heappop(open_list)

            if current_pos == goal:
                self.final_cost = cost_so_far
                return path

            if current_pos in visited:
                continue
            visited.add(current_pos)

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current_pos):
                if neighbor not in visited:
                    new_cost = cost_so_far + move_cost
                    h_neighbor = self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (h_neighbor, new_cost, neighbor, path + [neighbor]))

        return None
