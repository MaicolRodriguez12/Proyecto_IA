import networkx as nx
from typing import Tuple


class cell:
    """
    Class that represents a cell in the grid.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True]  # Top, Right, Bottom, Left

    def __repr__(self):
        return f"cell({self.x}, {self.y})"
    def __str__(self):
        return f"cell({self.x}, {self.y})"

    def is_wall(self, direction: str) -> bool:
        """
        Check if the cell has a wall in the given direction.
        """
        directions = {'top': 0, 'right': 1, 'bottom': 2, 'left': 3}
        return self.walls[directions[direction]]
    
    def is_cheese(self) -> bool:
        """
        Check if the cell is cheese.
        """
        return self.cheese
    
    def set_cheese(self, cheese: bool):
        """
        Set the cell as cheese.
        """
        self.cheese = cheese
        """
        Set the cell as cheese.
        """ 
    
    def position(self) -> Tuple[int, int]:
        """
        Get the position of the cell.
        """
        return (self.x, self.y)
    
    

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.graph = nx.grid_2d_graph(rows, columns)

    def show_nodes(self):
        return list(self.graph.nodes)
    
    def show_neighbors(self, node):
        if node in self.graph:
            return list(self.graph.neighbors(node))
        else:
            return []

    def lock_cell(self, node):
        if node in self.graph:
            neighbors = list(self.graph.neighbors(node))
            for neighbor in neighbors:
                self.graph.remove_edge(node, neighbor)

    def delete_connection(self, node1, node2):
        if self.graph.has_edge(node1, node2):
            self.graph.remove_edge(node1, node2)

    def add_connection(self, node1, node2):
        if node1 in self.graph and node2 in self.graph:
            self.graph.add_edge(node1, node2)


