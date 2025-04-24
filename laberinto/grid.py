import networkx as nx
from .cell import Cell
from typing import Tuple

class Grid:
    def __init__(self, rows: int, columns: int):
        self.traps = 0 #num trampas
        self.changed = False
        self.walls = 0 #num paredes
        self.rows = rows
        self.columns = columns
        self.graph = nx.Graph()
        for x in range(rows):
            for y in range(columns):
                coord = (x, y)
                self.graph.add_node(coord, cell=Cell(x, y))
        for x in range(rows):
            for y in range(columns):
                coord = (x, y)
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    n = (x + dx, y + dy)
                    if 0 <= n[0] < rows and 0 <= n[1] < columns:
                        self.graph.add_edge(coord, n)

    def get_cell(self, coord: Tuple[int,int]) -> Cell:
        return self.graph.nodes[coord]['cell']

    def get_neighbors(self, coord: Tuple[int,int]):
        return list(self.graph.neighbors(coord))
    
    def get_weighted_neighbors(self, coord):
        neighbors = []
        for n in self.graph.neighbors(coord):
            trap_type = self.get_cell(n).trap_type
            cost = {'gato': 5, 'ratonera': 3, '': 1}.get(trap_type, 1)
            neighbors.append((n, cost))
        return neighbors

    def set_wall(self, coord: Tuple[int,int], direction: str, value: bool):
        self.walls += 1 if value else -1
        cell = self.get_cell(coord)
        cell.set_wall(direction, value)
        deltas = {'top':(-1,0), 'bottom':(1,0), 'left':(0,-1), 'right':(0,1)}
        dx, dy = deltas[direction]
        neighbor = (coord[0] + dx, coord[1] + dy)
        if value and self.graph.has_edge(coord, neighbor):
            self.graph.remove_edge(coord, neighbor)
        elif not value and coord in self.graph and neighbor in self.graph:
            self.graph.add_edge(coord, neighbor)
        

    def lock_cell(self, coord: Tuple[int,int]):
        for d in ['top','right','bottom','left']:
            self.set_wall(coord, d, True)
    
    def set_trap(self, coord: Tuple[int,int], trap_type: str):
        self.traps += 1
        cell = self.get_cell(coord)
        cell.set_trap(trap_type)