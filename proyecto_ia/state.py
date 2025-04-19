from typing import List, Tuple
from .maze import Maze  # ← Importación relativa corregida

class State:
    """
    Representa un estado en la búsqueda:
    - agent_pos: posición actual del agente (x,y)
    - maze: referencia al objeto Maze (con su grid y la posición del queso)
    """

    def __init__(self, agent_pos: Tuple[int, int], maze: Maze):
        self.agent_pos: Tuple[int, int] = agent_pos
        self.maze: Maze = maze
        # la posición del queso puede cambiar dinámicamente
        self.cheese: Tuple[int, int] = maze.cheese

    def is_goal(self) -> bool:
        """Comprueba si el agente ha llegado al queso."""
        return self.agent_pos == self.cheese

    def successors(self) -> List[Tuple['State', int]]:
        """
        Genera los estados vecinos junto con su costo (1 por movimiento).
        Movimientos: arriba, abajo, izquierda, derecha.
        """
        x, y = self.agent_pos
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        succ = []
        for nx, ny in neighbors:
            if not self.maze.is_wall(nx, ny):
                new_state = State((nx, ny), self.maze)
                succ.append((new_state, 1))
        return succ

    def __hash__(self) -> int:
        """
        Hash basado en posición del agente, queso y configuración del laberinto.
        Permite usar estados en conjuntos/diccionarios.
        """
        grid_tuple = tuple(tuple(row) for row in self.maze.grid)
        return hash((self.agent_pos, self.cheese, grid_tuple))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return False
        return (
            self.agent_pos == other.agent_pos
            and self.cheese == other.cheese
            and self.maze.grid == other.maze.grid
        )

