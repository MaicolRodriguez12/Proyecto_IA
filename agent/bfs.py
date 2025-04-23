from collections import deque
from .SearchAlgorithm import SearchAlgorithm

# Implementación de búsqueda por amplitud (BFS)
class BFS(SearchAlgorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self.explored_cells = []  # Lista de celdas que se recorren

    def find_path(self, start, goal):
        queue = deque([(start, [start], 0)])  # (posición, camino, costo acumulado)
        self.visited.clear()
        self.explored_cells.clear()

        while queue:
            current_pos, path, total_cost = queue.popleft()

            # Marcar la celda como recorrida (visual)
            current_cell = self.grid.get_cell(current_pos)
            current_cell.make_traversed((135, 206, 250))  # Azul claro para BFS

            # Guardar la celda como explorada
            self.explored_cells.append(current_pos)

            if current_pos == goal:
                self.final_cost = total_cost
                return path

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current_pos):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], total_cost + move_cost))

        # No se encontró un camino
        return None
