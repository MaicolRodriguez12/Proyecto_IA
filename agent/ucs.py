from .SearchAlgorithm import SearchAlgorithm
import heapq

class UCS(SearchAlgorithm):
    def __init__(self, grid):
        super().__init__(grid)  
        self.final_cost = 0  
        self.explored_cells = []  

    def find_path(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start))  
        g_cost = {start: 0}  
        came_from = {}  
        self.visited.clear()
        self.explored_cells.clear()

        while open_list:
            cost, current = heapq.heappop(open_list)  

            if current in self.visited:
                continue
            self.visited.add(current)

            cell = self.grid.get_cell(current)
            cell.make_traversed((255, 105, 180))  
            self.explored_cells.append(current)

            if current == goal:
                self.final_cost = g_cost[current]
                path = [goal]
                while path[-1] in came_from:
                    path.append(came_from[path[-1]])  
                return list(reversed(path))  

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current):
                new_cost = g_cost[current] + move_cost  

                if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(open_list, (new_cost, neighbor))

        return None 
