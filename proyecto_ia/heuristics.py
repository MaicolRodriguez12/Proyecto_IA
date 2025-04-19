from .state import State  # Importación relativa

def manhattan(state: State) -> float:
    """
    Heurística de Manhattan: distancia del agente al queso.
    """
    x1, y1 = state.agent_pos
    x2, y2 = state.cheese
    return abs(x1 - x2) + abs(y1 - y2)
