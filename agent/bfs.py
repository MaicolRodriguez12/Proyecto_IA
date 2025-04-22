# author: Yeifer Ronaldo Muñoz Valencia
from collections import deque
from .SearchAlgorithm import SearchAlgorithm
    
# Implementación de búsqueda por amplitud (BFS)
class BFS(SearchAlgorithm):
    def find_path(self, start, goal):
        queue = deque([(start, [start])])  # (posición, camino)
        self.visited.clear()

        while queue:
            current_pos, path = queue.popleft()
            if current_pos == goal:
                return path  # Camino encontrado

            for neighbor in self.get_neighbors(current_pos):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None  # No hay camino