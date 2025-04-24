from agent.Agent import Agent

class AdaptiveAgent:
    def __init__(self, laberinto, start, goal, initial_algorithm="A*"):
        self.laberinto = laberinto
        self.start = start
        self.goal = goal
        self.current_algorithm = initial_algorithm
        self.algorithms = ["A*", "UCS", "BFS", "Greedy", "DFS"] 
        self.agent = Agent(self.laberinto, self.current_algorithm)
        self.metrics = {
            "replan_time": 0,
            "blocked_nodes": 0,
            "cost_history": [],
            "change_counter": 0
        }
        self.plan_path() 
        self.visited_cells = []
        self.traversal_cost = 0

    def plan_path(self):
        import time
        t0 = time.time()
        self.agent = Agent(self.laberinto, self.current_algorithm)
        self.agent.find_path(self.start, self.goal)
        t1 = time.time()
        self.metrics["replan_time"] = (t1 - t0) * 1000
        self.metrics["cost_history"].append(self.agent.total_cost)

    def get_next_move(self):
        next_pos = self.agent.get_next_move()
        if next_pos:
            self.visited_cells.append(next_pos)

            trap_type = self.laberinto.get_cell(next_pos).trap_type
            cost = {'gato': 5, 'ratonera': 3, '': 1}.get(trap_type, 1)
            self.traversal_cost += cost
        return next_pos


    def select_algorithm(self):
        self.evaluate_algorithm()

    def evaluate_algorithm(self):
        print("\n--- Evaluación de algoritmo ---")
        print(f"Algoritmo actual: {self.current_algorithm}")
        print(f"Pasos actuales: {self.agent.total_steps}")
        print(f"Costo total actual: {self.agent.total_cost}")
    # Calculamos las puntuaciones para los cinco algoritmos
        scores = {
            "A*": self.calculate_astar_score(),
            "UCS": self.calculate_ucs_score(),
            "BFS": self.calculate_bfs_score(),
            "Greedy": self.calculate_greedy_score(),
            "DFS": self.calculate_dfs_score()
        }
        print(f"Puntuaciones: {scores}") 
        best_algorithm = max(scores, key=scores.get)
        print(f"Mejor algoritmo seleccionado: {best_algorithm}") 

        if scores[best_algorithm] - scores[self.current_algorithm] > 0.0001:
            self.current_algorithm = best_algorithm
            self.agent.set_algorithm(best_algorithm)
            self.metrics["change_counter"] += 1
            self.plan_path()


    def calculate_astar_score(self):
        time_score = max(0, 10 - self.metrics["replan_time"] * 0.1) 
        step_score = max(0, 10 - self.agent.total_steps * 0.05) 
        return time_score + step_score

    def calculate_ucs_score(self):
        cost_score = max(0, 10 - self.agent.total_cost * 0.1)  
        step_score = max(0, 10 - self.agent.total_steps * 0.05)  
        return cost_score + step_score

    def calculate_bfs_score(self):
        blocked_score = max(0, 10 - self.metrics["blocked_nodes"] * 0.5)
        step_score = max(0, 10 - self.agent.total_steps * 0.1)
        return blocked_score + step_score

    def calculate_greedy_score(self):
        cost_score = max(0, 10 - self.agent.total_cost * 0.1) 
        blocked_score = max(0, 10 - self.metrics["blocked_nodes"] * 0.5)
        return cost_score + blocked_score

    def calculate_dfs_score(self):
        step_score = max(0, 10 - self.agent.total_steps * 0.05)
        cost_score = max(0, 10 - self.agent.total_cost * 0.05) 
        return step_score + cost_score



    @property
    def total_steps(self):
        return self.agent.total_steps

    @property
    def total_cost(self):
        return self.agent.total_cost

    @property
    def algorithm(self):
        return self.agent.algorithm
