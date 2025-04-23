# cell.py
from typing import Tuple

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        # cambio: uso dict en vez de lista, evita índices mágicos
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        # inicializar atributos faltantes para A*
        self.base_cost = 1
       # costo por defecto de la celda
        self.cheese = False  # si la celda contiene el 'queso'
        self.trap_type = None
        self.trap_costs = {'ratonera': 3, 'gato': 5}
        self.is_trap  = False
        self.cost = self.base_cost
        self.cheese = False

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
    __str__ = __repr__

    def is_wall(self, direction: str) -> bool:
        return self.walls.get(direction, True)

    def set_wall(self, direction: str, value: bool):
        # mantener sincronizado grafo y walls
        self.walls[direction] = value
        # grid tendrá un hook para actualizar el grafo (ver Grid.set_wall)

    def is_cheese(self) -> bool:
        return self.cheese

    def set_cheese(self, cheese: bool):
        self.cheese = cheese

    def set_visited(self, visited: bool):
        self.visited = visited

    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def set_trap(self, trap: str):
        """Asigna o quita trampa. trap in (None,'ratonera','gato')"""
        self.trap_type = trap
        if trap in self.trap_costs:
            self.cost = self.base_cost + self.trap_costs[trap]
        else:
            self.cost = self.base_cost
    
    def is_trap(self) -> bool:
        return self.trap_type is not None