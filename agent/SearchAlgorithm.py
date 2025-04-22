# author: Yeifer Ronaldo Muñoz Valencia

class SearchAlgorithm:
    def __init__(self, grid):
        self.grid = grid  # Laberinto (objeto Grid)
        self.visited = set()  # Nodos visitados para evitar ciclos
        self.grid.changed = False

    def get_neighbors(self, position):
        """Obtiene movimientos válidos desde una posición"""
        x, y = position
        neighbors = []
        # Movimientos posibles (arriba, abajo, izquierda, derecha)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid.width and 0 <= ny < self.grid.height:
                if not self.grid.cells[nx][ny].is_wall:
                    neighbors.append((nx, ny))
        return neighbors