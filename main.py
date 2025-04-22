#Proyecto de IA
#Autores: Yeifer Ronaldo Muñoz Valencia
#         Juan Carlos Rojas Quintero
#         Michael Steven Rodriguez Arana

import json
from laberinto.grid import Grid
from agent.dynamicAgent import AgentDynamic as Agent

def main():
    # 1. Cargar configuración
    with open("configs/ejemplo1.json") as f:
        cfg = json.load(f)

    # 2. Inicializar grid y agente
    grid_obj = Grid(cfg["height"], cfg["width"], config=cfg)
    start = tuple(cfg.get("start", (0,0)))
    goal = tuple(cfg.get("goal", (cfg["height"]-1, cfg["width"]-1)))
    agent = Agent(grid_obj.grid, start, goal)

    # 3. Bucle de prueba sin gráfica
    for step in range(10):
        grid_obj.random_toggle_wall()    # simulamos cambio
        agent.graph = agent._build_graph()
        path = agent.compute_bfs()
        print(f"Step {step}: Path length = {len(path) if path else 'No path'}")

if __name__ == "__main__":
    main()
