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
        stack = [(start, [start], 0)]  # (posición, camino, costo acumulado)
        self.visited.clear()

        while stack:
          
            current_pos, path = stack.pop()  # Último elemento (LIFO)

            # Pinta la celda actual
            cell = self.laberinto.get_cell(current_pos)
            if current_pos != start and current_pos != goal:
                cell.make_traversed(self.dfs_color)
                pygame.display.update()
                time.sleep(0.03)


            current_pos, path, total_cost = stack.pop()
            if current_pos == goal:
                self.final_cost = total_cost
                return path

            for neighbor, move_cost in self.grid.get_weighted_neighbors(current_pos):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor], total_cost + move_cost))

        return None
