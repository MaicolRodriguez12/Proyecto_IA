from agent.bfs import BFS
from agent.dfs import DFS
from agent.aStar import AStar
from agent.ucs import UCS
from agent.greedy import Greedy

class Agent:
    def __init__(self, grid, algorithm="A*"):
        self.grid = grid
        self.algorithm = algorithm  
        self.path = []              
        self.current_step = 0  
        self.current_strategy = algorithm  
        self.stuck_counter = 0             
        self.explored = []           
        self.total_steps = 0         
        print(f"Algoritmo inicial: {self.algorithm}") 


    def set_algorithm(self, algorithm):
        """Establecer el algoritmo actual del agente"""
        print(f"Algoritmo actualizado a: {algorithm}")  
        self.algorithm = algorithm
        self.current_strategy = algorithm  

    def find_path(self, start, goal):
        """Encuentra el camino usando el algoritmo seleccionado"""
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

        result = searcher.find_path(start, goal)
        self.path = result if result else []
        self.explored = getattr(searcher, "explored_cells", [])  
        self.current_step = 0
        self.total_steps = len(self.path) - 1 if self.path else 0
        self.total_cost = getattr(searcher, "final_cost", 0)

    def get_next_move(self):
        """Devuelve la siguiente posición en el camino o celdas exploradas si no hay camino"""
        if self.path and self.current_step < len(self.path):
            next_pos = self.path[self.current_step]
            self.current_step += 1
            return next_pos
        elif not self.path and self.current_step < len(self.explored):
            next_pos = self.explored[self.current_step]
            self.current_step += 1
            return next_pos
        return None
