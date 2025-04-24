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
        self.current_step = 0  
        self.current_strategy = algorithm   # Paso actual en el camino
        self.stuck_counter = 0             
        self.explored = []           # Celdas recorridas incluso si no se encuentra camino
        self.total_steps = 0         # Asegurarnos de inicializar este atributo
        print(f"Algoritmo inicial: {self.algorithm}")  # Para depuración

    def evaluate_environment(self):
        """Decide el mejor algoritmo basado en el entorno"""
        # Condición 1: Queso móvil
        if self.grid.cheese_moves > 2:
            return 'A*'
        
        # Condición 2: Muchos obstáculos
        if self.grid.traps / (self.grid.rows * self.grid.columns) > 0.3:
            return 'BFS'
        
        # Condición 3: Costos altos
        if self.grid.get_average_cost() > 2.5:
            return 'UCS'
        
        return self.current_strategy  # Mantener estrategia actual

    def replanify(self):
        """Reinicia la búsqueda si hay cambios"""
        if self.grid.changes:
            new_strategy = self.evaluate_environment()
            if new_strategy != self.current_strategy:
                print(f"Cambiando estrategia a {new_strategy}")
                self.current_strategy = new_strategy
                self.set_algorithm(new_strategy)  # Asegurarse de que se actualice el algoritmo
            self.find_path(self.current_position, self.grid.cheese_position)
            self.grid.changes = False

    def set_algorithm(self, algorithm):
        """Establecer el algoritmo actual del agente"""
        print(f"Algoritmo actualizado a: {algorithm}")  # Para depuración
        self.algorithm = algorithm
        self.current_strategy = algorithm  # Asegurarse de que el algoritmo y la estrategia coincidan

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
        self.explored = getattr(searcher, "explored_cells", [])  # Guardar celdas exploradas si no hay camino

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
