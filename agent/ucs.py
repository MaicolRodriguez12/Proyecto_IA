# author: Yeifer Ronaldo Muñoz Valencia

import heapq

class UCS:
    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start, goal):
        priority_queue = []
        heapq.heappush(priority_queue, (0, start, [start]))  # (costo acumulado, posición, camino)
        visited = {}  # Guarda el mejor costo para cada posición

        while priority_queue:
            current_cost, current_pos, path = heapq.heappop(priority_queue)

            if current_pos == goal:
                return path

            if current_pos in visited and visited[current_pos] <= current_cost:
                continue  # Ya existe un camino más barato
            visited[current_pos] = current_cost

            for neighbor in self.get_neighbors(current_pos):
                cell = self.grid.cells[neighbor[0]][neighbor[1]]
                if cell.is_wall:
                    continue  # Ignorar paredes
                new_cost = current_cost + cell.cost
                new_path = path + [neighbor]
                heapq.heappush(priority_queue, (new_cost, neighbor, new_path))

        return None