from typing import Tuple, List, Optional
import numpy as np
import networkx as nx

class Agent:
    def __init__(self, grid: np.ndarray, start: Tuple[int,int], goal: Tuple[int,int]):
        """
        grid: numpy.ndarray 2D donde 0=libre, 1=muro, 2=meta
        start: coordenadas (y,x) de inicio
        goal: coordenadas (y,x) de la meta
        """
        self.grid = grid                                              # :contentReference[oaicite:0]{index=0}
        self.position = start
        self.goal = goal
        self.path: List[Tuple[int,int]] = []                          # camino actual
        self.graph = self._build_graph()                              # grafo derivado de la grilla
        self.strategy = 'BFS'                                         # algoritmo activo

    def _build_graph(self) -> nx.Graph:
        """
        Reconstruye el grafo 2D a partir de self.grid, 
        eliminando nodos que son muros (valor 1).
        """
        G = nx.grid_2d_graph(*self.grid.shape)                        # :contentReference[oaicite:1]{index=1}
        for y,x in zip(*np.where(self.grid == 1)):
            G.remove_node((y, x))
        return G

    def compute_bfs(self) -> Optional[List[Tuple[int,int]]]:
        """
        Ejecuta BFS sobre self.graph desde self.position hasta self.goal.
        Devuelve la lista de nodos en el camino o None si no hay ruta.
        """
        try:
            # bfs_edges genera aristas en orden BFS; reconstruimos camino completo
            edges = list(nx.bfs_edges(self.graph, self.position))    # :contentReference[oaicite:2]{index=2}
            path_nodes = [self.position] + [v for (_,v) in edges]
            if self.goal in path_nodes:
                idx = path_nodes.index(self.goal)
                return path_nodes[:idx+1]
        except Exception:
            pass
        return None

    def move_step(self):
        """
        Avanza un paso según el camino calculado. Recalcula si es necesario.
        """
        # Si no tenemos camino o la meta cambió, calculamos de nuevo
        if not self.path or self.path[-1] != self.goal:
            self.path = self.compute_bfs()                            # :contentReference[oaicite:3]{index=3}

        if self.path and len(self.path) > 1:
            # Avanzar al siguiente nodo
            self.position = self.path.pop(1)
        else:
            # Sin camino encontrado → estrategia de adaptación
            self.adapt_strategy()                                     # :contentReference[oaicite:4]{index=4}

    def adapt_strategy(self):
        """
        Lógica simple para cambiar de BFS a otra estrategia.
        (Aquí solo ejemplificamos cambio de nombre; completo en fase A*).
        """
        if self.strategy == 'BFS':
            self.strategy = 'A*'
        else:
            self.strategy = 'BFS'
