from .SearchAlgorithm import SearchAlgorithm

class DFS(SearchAlgorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self.explored_cells = []  # Lista de celdas exploradas

    def find_path(self, start, goal):
        stack = [(start, [start], 0)]  # (posición, camino, costo acumulado)
        self.visited.clear()
        self.explored_cells.clear()

        while stack:
            current_pos, path, total_cost = stack.pop()

            current_cell = self.grid.get_cell(current_pos)
            current_cell.make_traversed((255, 0, 0))  # Rojo para DFS

            # Registrar la celda como explorada
            self.explored_cells.append(current_pos)

            if current_pos == goal:
                self.final_cost = total_cost
                return path

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current_pos):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor], total_cost + move_cost))

        return None  # No se encontró camino
