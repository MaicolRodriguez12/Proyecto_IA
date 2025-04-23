# author: Yeifer Ronaldo Muñoz Valencia

from .SearchAlgorithm import SearchAlgorithm
import pygame
import time

# Implementación de búsqueda por profundidad (DFS)
class DFS(SearchAlgorithm):
    def __init__(self, laberinto):
        super().__init__(laberinto)
        self.laberinto = laberinto
        self.dfs_color = (144, 238, 144)  # Verde claro (light green)

    def find_path(self, start, goal):
        stack = [(start, [start])]  # (posición, camino)
        self.visited.clear()

        while stack:
            current_pos, path = stack.pop()  # Último elemento (LIFO)

            # Pinta la celda actual
            cell = self.laberinto.get_cell(current_pos)
            if current_pos != start and current_pos != goal:
                cell.make_traversed(self.dfs_color)
                pygame.display.update()
                time.sleep(0.03)

            if current_pos == goal:
                return path

            for neighbor in self.get_neighbors(current_pos):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

        return None
