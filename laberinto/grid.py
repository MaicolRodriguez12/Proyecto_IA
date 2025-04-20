import numpy as np
from typing import Tuple, Dict, Any

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
    
    