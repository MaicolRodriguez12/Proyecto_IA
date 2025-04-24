from collections import deque
from .SearchAlgorithm import SearchAlgorithm

class BFS(SearchAlgorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self.explored_cells = [] 

    def find_path(self, start, goal):
        queue = deque([(start, [start], 0)])  
        self.visited.clear()
        self.explored_cells.clear()

        while queue:
            current_pos, path, total_cost = queue.popleft()

            current_cell = self.grid.get_cell(current_pos)
            current_cell.make_traversed((135, 206, 250))  

            self.explored_cells.append(current_pos)

            if current_pos == goal:
                self.final_cost = total_cost
                return path

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current_pos):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], total_cost + move_cost))

        return None
