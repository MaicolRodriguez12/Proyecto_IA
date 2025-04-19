from .maze import Maze

def select_initial_strategy(maze: Maze) -> str:
    wall_count = sum(row.count(1) for row in maze.grid)
    total_cells = len(maze.grid) * len(maze.grid[0])
    wall_ratio = wall_count / total_cells

    if wall_ratio > 0.4:
        return "dfs"
    elif wall_ratio <= 0.2:  # antes era < 0.2
        return "astar"
    else:
        return "bfs"

def should_switch_strategy(history, window: int = 10) -> bool:
    if len(history) < window:
        return False
    recent = history[-window:]
    failures = sum(1 for result in recent if result is None or (isinstance(result, list) and len(result) > 100))
    return failures >= window // 2