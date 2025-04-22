# author: Yeifer Ronaldo Muñoz Valencia
from laberinto.grid import Grid

class SearchAlgorithm:
    def __init__(self, grid):
        self.grid = grid  # Laberinto (objeto Grid)
        self.visited = set()  # Nodos visitados para evitar ciclos
        self.grid.changed = False

    def get_neighbors(self, position):
        return self.grid.get_neighbors(position)