# author: Yeifer Ronaldo Muñoz Valencia

from .SearchAlgorithm import SearchAlgorithm

# Implementación de búsqueda por profundidad (DFS)
class DFS(SearchAlgorithm):
    def find_path(self, start, goal):
        stack = [(start, [start])]  # (posición, camino)
        self.visited.clear()

        while stack:
            current_pos, path = stack.pop()  # Último elemento (LIFO)
            if current_pos == goal:
                return path

            for neighbor in self.get_neighbors(current_pos):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

        return None