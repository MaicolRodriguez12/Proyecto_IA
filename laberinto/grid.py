import numpy as np
from typing import Tuple, Dict, Any

class Grid:
    def __init__(self, height: int, width: int, config: Dict[str, Any] = None):
        # 0 = libre, 1 = muro, 2 = meta
        self.height = height
        self.width = width
        self.grid = np.zeros((height, width), dtype=int)
        if config:
            self.load_config(config)

    def load_config(self, cfg: Dict[str, Any]):
        # Carga muros, start, goal y reglas dinámicas desde JSON
        for y, x in cfg.get("walls", []):
            self.grid[y, x] = 1
        gy, gx = cfg.get("goal", (self.height-1, self.width-1))
        self.grid[gy, gx] = 2
        # Guarda reglas dinámicas en self.dynamic_rules...
    
    def random_toggle_wall(self):
        # Ejemplo: invierte el estado de una celda aleatoria
        i, j = np.random.randint(0, self.height), np.random.randint(0, self.width)
        if self.grid[i, j] in (0, 1):
            self.grid[i, j] = 1 - self.grid[i, j]