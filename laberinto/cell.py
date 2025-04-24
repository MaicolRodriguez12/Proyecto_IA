from typing import Tuple

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.base_cost = 1
        self.cheese = False
        self.trap_type = None
        self.trap_costs = {'ratonera': 3, 'gato': 5}
        self.is_trap = False
        self.cost = self.base_cost
        self.is_traversed = False
        self.traversed_color = None

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
    __str__ = __repr__

    def is_wall(self, direction: str) -> bool:
        return self.walls.get(direction, True)

    def set_wall(self, direction: str, value: bool):
        self.walls[direction] = value

    def is_cheese(self) -> bool:
        return self.cheese

    def set_cheese(self, cheese: bool):
        self.cheese = cheese

    def set_visited(self, visited: bool):
        self.visited = visited

    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def set_trap(self, trap: str):
        """Asigna o quita trampa. trap in (None, 'ratonera', 'gato')"""
        self.trap_type = trap
        if trap in self.trap_costs:
            self.cost = self.base_cost + self.trap_costs[trap]
        else:
            self.cost = self.base_cost
    
    def remove_trap(self):
        """Elimina cualquier trampa de la celda."""
        self.trap_type = None
        self.cost = self.base_cost
    
    def is_trap(self) -> bool:
        return self.trap_type is not None

    # Método para marcar la celda como recorrida
    def make_traversed(self, color):
        self.traversed_color = color
        self.is_traversed = True

