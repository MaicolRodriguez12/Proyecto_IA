# author: Yeifer Ronaldo Muñoz Valencia

from .bfs import BFS
from .dfs import DFS
from .aStar import AStar

class AgentDynamic:
    """Agente que cambia de estrategia según su estado"""
    def __init__(self, grid):
        self.grid = grid  # Laberinto dinámico
        self.current_strategy = "A*"  # Algoritmo inicial (justificado por eficiencia)
        self.stuck_steps = 0  # Contador de pasos sin progreso
        self.position = None  # Posición actual del agente
        self.path_history = []  # Historial de posiciones

    def update_position(self, new_position):
        """Actualiza la posición y verifica si está atascado"""
        self.path_history.append(new_position)
        self.position = new_position

        # Si los últimos 10 pasos están en un radio pequeño, está atascado
        if len(self.path_history) > 10:
            recent_positions = self.path_history[-10:]
            if len(set(recent_positions)) < 3:  # Pocas posiciones únicas
                self.stuck_steps += 1
            else:
                self.stuck_steps = 0

    def switch_strategy(self):
        """Cambia de algoritmo según las condiciones"""
        if self.stuck_steps >= 5:  # Ejemplo: 5 pasos sin progreso
            if self.current_strategy == "A*":
                self.current_strategy = "BFS"  # Exploración amplia
            elif self.current_strategy == "BFS":
                self.current_strategy = "DFS"  # Exploración profunda
            else:
                self.current_strategy = "A*"  # Volver a A*
            self.stuck_steps = 0  # Reiniciar contador

    def find_path(self, goal):
        """Ejecuta el algoritmo actual y devuelve la ruta"""
        if self.current_strategy == "A*":
            algorithm = AStar(self.grid)
        elif self.current_strategy == "BFS":
            algorithm = BFS(self.grid)
        elif self.current_strategy == "DFS":
            algorithm = DFS(self.grid)

        path = algorithm.find_path(self.position, goal)
        return path
