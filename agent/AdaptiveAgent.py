from agent.Agent import Agent

class AdaptiveAgent:
    def __init__(self, laberinto, start, goal, initial_algorithm="A*"):
        self.laberinto = laberinto
        self.start = start
        self.goal = goal
        self.current_algorithm = initial_algorithm
        self.algorithms = ["A*", "UCS", "BFS"]
        self.agent = Agent(self.laberinto, self.current_algorithm)
        self.metrics = {
            "replan_time": 0,
            "blocked_nodes": 0,
            "cost_history": [],
            "change_counter": 0
        }
        self.plan_path()  # Planificamos el camino inicial

    def plan_path(self):
        import time
        t0 = time.time()
        self.agent = Agent(self.laberinto, self.current_algorithm)
        self.agent.find_path(self.start, self.goal)
        t1 = time.time()
        self.metrics["replan_time"] = (t1 - t0) * 1000
        self.metrics["cost_history"].append(self.agent.total_cost)

    def get_next_move(self):
        return self.agent.get_next_move()

    def select_algorithm(self):
        self.evaluate_algorithm()

    def evaluate_algorithm(self):
        scores = {
            "A*": self.calculate_astar_score(),
            "UCS": self.calculate_ucs_score(),
            "BFS": self.calculate_bfs_score()
        }
        best_algorithm = max(scores, key=scores.get)
        if scores[best_algorithm] - scores[self.current_algorithm] > 2:
            self.current_algorithm = best_algorithm
            self.agent.set_algorithm(best_algorithm)
            self.metrics["change_counter"] += 1
            self.plan_path()

    def calculate_astar_score(self):
        return 10 - self.metrics["change_counter"] * 0.5

    def calculate_ucs_score(self):
        return 8 + sum(1 for cost in self.metrics["cost_history"] if cost >= 3)

    def calculate_bfs_score(self):
        return 6 + self.metrics["blocked_nodes"] * 0.8

    @property
    def total_steps(self):
        return self.agent.total_steps

    @property
    def total_cost(self):
        return self.agent.total_cost

    @property
    def algorithm(self):
        return self.agent.algorithm
