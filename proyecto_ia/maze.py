# maze.py
import random
from typing import Tuple, List

class Maze:
    """
    Laberinto dinámico:
    - grid[y][x] == 0: celda libre
    - grid[y][x] == 1: pared
    - cheese: posición actual del queso (meta).
    """

    def __init__(self, width: int, height: int, obstacle_prob: float = 0.2):
        self.width = width
        self.height = height
        # Genera matriz aleatoria de obstáculos
        self.grid: List[List[int]] = [
            [1 if random.random() < obstacle_prob else 0 for _ in range(width)]
            for _ in range(height)
        ]
        # Asegura que haya al menos una celda libre
        self.cheese: Tuple[int,int] = self.random_empty_cell()

    def random_empty_cell(self) -> Tuple[int,int]:
        """Devuelve coordenadas (x,y) de una celda libre al azar."""
        while True:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if self.grid[y][x] == 0:
                return (x, y)

    def is_wall(self, x: int, y: int) -> bool:
        """¿Es posición (x,y) un muro o está fuera de rangos?"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        return self.grid[y][x] == 1

    def add_wall(self, x: int, y: int) -> None:
        """Añade un muro en (x,y) si está dentro del laberinto."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 1

    def remove_wall(self, x: int, y: int) -> None:
        """Elimina un muro en (x,y), dejándolo libre."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 0

    def move_cheese(self) -> None:
        """Mueve la meta (queso) a otra celda libre al azar."""
        self.cheese = self.random_empty_cell()
