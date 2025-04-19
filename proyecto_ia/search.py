import heapq
from collections import deque
from itertools import count
from typing import Callable, Dict, List, Optional, Tuple

from .state import State


def bfs(initial: State) -> Optional[List[Tuple[int, int]]]:
    visited = set()
    queue = deque([(initial, [])])
    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        if current.is_goal():
            return path + [current.agent_pos]
        for neighbor, cost in current.successors():
            queue.append((neighbor, path + [current.agent_pos]))
    return None


def dfs(initial: State, max_depth: int = 1000) -> Optional[List[Tuple[int, int]]]:
    visited = set()
    stack = [(initial, [], 0)]
    while stack:
        current, path, depth = stack.pop()
        if current in visited or depth > max_depth:
            continue
        visited.add(current)
        if current.is_goal():
            return path + [current.agent_pos]
        for neighbor, cost in current.successors():
            stack.append((neighbor, path + [current.agent_pos], depth + 1))
    return None


def astar(initial: State, heuristic: Callable[[State], float]) -> Optional[List[Tuple[int, int]]]:
    open_set = []
    counter = count()
    heapq.heappush(open_set, (heuristic(initial), next(counter), 0, initial, []))
    visited = set()
    while open_set:
        _, _, g, current, path = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        if current.is_goal():
            return path + [current.agent_pos]
        for neighbor, cost in current.successors():
            heapq.heappush(open_set, (
                g + cost + heuristic(neighbor),
                next(counter),
                g + cost,
                neighbor,
                path + [current.agent_pos]
            ))
    return None