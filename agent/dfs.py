# author: Yeifer Ronaldo Muñoz Valencia

from .SearchAlgorithm import SearchAlgorithm

# Implementación de búsqueda por profundidad (DFS)
class DFS(SearchAlgorithm):
    def find_path(self, start, goal):
        stack = [(start, [start], 0)]  # (posición, camino, costo acumulado)
        self.visited.clear()

        while stack:
            current_pos, path, total_cost = stack.pop()
            if current_pos == goal:
                self.final_cost = total_cost
                return path

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current_pos):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor], total_cost + move_cost))

        return None
