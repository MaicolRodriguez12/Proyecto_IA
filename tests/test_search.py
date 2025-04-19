# tests/test_search.py
import pytest
from proyecto_ia.maze import Maze
from proyecto_ia.state import State
from proyecto_ia.search import bfs, dfs, astar
from proyecto_ia.heuristics import manhattan

@pytest.fixture
def simple_maze():
    # Laberinto 3×3 sin obstáculos y queso en (2,2)
    m = Maze(3, 3, obstacle_prob=0)
    m.cheese = (2, 2)
    return m

@pytest.fixture
def start_state(simple_maze):
    # Estado inicial en (0,0)
    return State((0, 0), simple_maze)

def test_bfs_shortest_path(start_state):
    path = bfs(start_state)
    # Comienza en (0,0) y termina en (2,2)
    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)
    # Longitud mínima esperada: 5 movimientos
    assert len(path) == 5

def test_dfs_with_limit_found(start_state):
    path = dfs(start_state, max_depth=10)
    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)

def test_astar_matches_bfs(start_state):
    path_astar = astar(start_state, manhattan)
    path_bfs = bfs(start_state)
    # Con heurística Manhattan en este laberinto sin obstáculos,
    # A* debe encontrar también el camino más corto
    assert path_astar == path_bfs
