import pytest
from proyecto_ia.maze import Maze

@pytest.fixture
def small_maze():
    return Maze(5, 5, obstacle_prob=0)

def test_random_empty_cell(small_maze):
    x, y = small_maze.random_empty_cell()
    assert 0 <= x < small_maze.width
    assert 0 <= y < small_maze.height

def test_add_remove_wall(small_maze):
    small_maze.add_wall(1, 1)
    assert small_maze.is_wall(1, 1)
    small_maze.remove_wall(1, 1)
    assert not small_maze.is_wall(1, 1)

def test_move_cheese(small_maze):
    old = small_maze.cheese
    small_maze.move_cheese()
    assert small_maze.cheese != old