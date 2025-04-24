from laberinto.grid import Grid

class SearchAlgorithm:
    def __init__(self, grid):
        self.grid = grid  
        self.visited = set()  
        self.grid.changed = False

    def get_neighbors(self, position):
        return self.grid.get_neighbors(position)