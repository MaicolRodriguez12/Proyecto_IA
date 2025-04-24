
class AdaptiveAgent:
    def __init__(self, grid):
        self.grid = grid
        self.current_algorithm = "A*"
        self.metrics = {
            "replan_time": 0,
            "blocked_nodes": 0,
            "cost_history": [],
            "change_counter": 0
        }
        self.path = []

    def evaluate_algorithm(self):
        scores = {
            "A*": self.calculate_astar_score(),
            "UCS": self.calculate_ucs_score(),
            "BFS": self.calculate_bfs_score()
        }
        best_algorithm = max(scores, key=scores.get)
        if scores[best_algorithm] - scores[self.current_algorithm] > 2:  # Umbral de histéresis
            self.current_algorithm = best_algorithm

    def calculate_astar_score(self):
        base_score = 10
        # Penalizar si hay muchos cambios recientes
        penalty = self.metrics["change_counter"] * 0.5
        # Bonificar si el costo ambiental es bajo
        bonus = (3 - self.grid.average_cost()) * 2
        return base_score - penalty + bonus

    def calculate_ucs_score(self):
        base_score = 8
        # Bonificar si hay costos altos en la ruta
        bonus = sum(1 for cost in self.metrics["cost_history"] if cost >= 3) * 1.5
        # Penalizar por tiempo de cálculo
        penalty = self.metrics["replan_time"] / 100
        return base_score + bonus - penalty

    def calculate_bfs_score(self):
        base_score = 6
        # Bonificar si hay bloqueos críticos
        bonus = self.metrics["blocked_nodes"] * 0.8
        # Penalizar si el entorno es dinámico
        penalty = self.metrics["change_counter"] * 0.6
        return base_score + bonus - penalty