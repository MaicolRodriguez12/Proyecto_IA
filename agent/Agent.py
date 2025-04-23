from agent.bfs import BFS
from agent.dfs import DFS
from agent.aStar import AStar
from agent.ucs import UCS
from agent.greedy import Greedy

class Agent:
    def __init__(self, grid, algorithm="A*"):
        self.grid = grid
        self.algorithm = algorithm  # Opciones: "BFS", "DFS", "A*", "UCS"
        self.path = []              # Camino precalculado
        self.current_step = 0       # Paso actual en el camino

    def set_algorithm(self, algorithm):
        """Cambia el algoritmo (usado antes de iniciar la búsqueda)"""
        self.algorithm = algorithm

    def find_path(self, start, goal):
        if self.algorithm == "BFS":
            searcher = BFS(self.grid)
        elif self.algorithm == "DFS":
            searcher = DFS(self.grid)
        elif self.algorithm == "UCS":
            searcher = UCS(self.grid)
        elif self.algorithm == "Greedy":
            searcher = Greedy(self.grid)
        else:  # A*
            searcher = AStar(self.grid)

        self.path = searcher.find_path(start, goal)
        self.current_step = 0

            # Guardar info de pasos y costo si el algoritmo lo provee
        self.total_steps = len(self.path) - 1 if self.path else 0
        self.total_cost = getattr(searcher, "final_cost", 0)

    def find_best_path(self, start, goal):
        algorithms = {
            "BFS": BFS(self.grid),
            "DFS": DFS(self.grid),
            "UCS": UCS(self.grid),
            "Greedy": Greedy(self.grid),
            "A*": AStar(self.grid)
        }

        best_path = None
        best_cost = float("inf")
        best_algo = None

        for name, algo in algorithms.items():
            path = algo.find_path(start, goal)
            if path:
                cost = getattr(algo, "final_cost", len(path) - 1)
                if cost < best_cost:
                    best_cost = cost
                    best_path = path
                    best_algo = name

        self.path = best_path
        self.algorithm = best_algo
        self.total_steps = len(best_path) - 1 if best_path else 0
        self.total_cost = best_cost
        self.current_step = 0

    def get_next_move(self):
        """Devuelve la siguiente posición en el camino precalculado"""
        if self.current_step < len(self.path):
            next_pos = self.path[self.current_step]
            self.current_step += 1
            return next_pos
        return None