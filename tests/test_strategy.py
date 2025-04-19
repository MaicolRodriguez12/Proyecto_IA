from proyecto_ia.maze import Maze
from proyecto_ia.strategy_selector import select_initial_strategy, should_switch_strategy

def test_select_initial_strategy_small():
    # Área 10×10 = 100 ≤ 900 → astar (ahora funciona con wall_ratio <= 0.2)
    m = Maze(10, 10, obstacle_prob=0)
    assert select_initial_strategy(m) == 'astar'

def test_select_initial_strategy_dense():
    # Mapa muy denso en muros → dfs
    m = Maze(10, 10, obstacle_prob=0.9)
    assert select_initial_strategy(m) == 'dfs'

def test_select_initial_strategy_medium():
    # Mapa con densidad media → bfs
    m = Maze(10, 10, obstacle_prob=0.3)
    assert select_initial_strategy(m) == 'bfs'

def test_should_switch_strategy_insufficient_history():
    history = [None] * 5  # Menos de 10 elementos
    assert not should_switch_strategy(history)

def test_should_switch_strategy_no_failures():
    # Todos los caminos son cortos, no se cambia estrategia
    history = [[(0, 0), (0, 1)]] * 12
    assert not should_switch_strategy(history)

def test_should_switch_strategy_stuck():
    # Simula 6 fallos (None) + 4 caminos largos
    history = [None] * 6 + [[(i, i) for i in range(150)]] * 4
    assert should_switch_strategy(history, window=10)