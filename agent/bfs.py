from collections import deque
from .SearchAlgorithm import SearchAlgorithm

# Implementación de búsqueda por amplitud (BFS)
class BFS(SearchAlgorithm):
    def find_path(self, start, goal):
        queue = deque([(start, [start], 0)])  # (posición, camino, costo acumulado)
        self.visited.clear()
        
        while queue:
            current_pos, path, total_cost = queue.popleft()  # Desempaquetar todo en una sola llamada

            # Llamar a make_traversed para marcar la celda recorrida con el color azul claro para BFS
            current_cell = self.grid.get_cell(current_pos)
            current_cell.make_traversed((135, 206, 250))  # Azul claro para BFS

            if current_pos == goal:
                self.final_cost = total_cost
                return path

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current_pos):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], total_cost + move_cost))

        return None  # No hay camino
