import pygame
import sys
from .maze import Maze
from .state import State
from .search import bfs, dfs, astar
from .heuristics import manhattan
from .strategy_selector import select_initial_strategy, should_switch_strategy

# Colores
COLOR_BG = (30, 30, 30)
COLOR_WALL = (50, 50, 50)
COLOR_FREE = (200, 200, 200)
COLOR_AGENT = (0, 200, 0)
COLOR_CHEESE = (200, 200, 0)
COLOR_FRONTIER = (50, 150, 250)
COLOR_EXPLORED = (150, 50, 250)

class GUI:
    def __init__(self, maze: Maze, cell_size=20, fps=10):
        pygame.init()
        self.maze = maze
        self.cell_size = cell_size
        self.fps = fps
        self.width = maze.width * cell_size
        self.height = maze.height * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Agente en Laberinto Dinámico')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, path=None, frontier=None, explored=None):
        self.screen.fill(COLOR_BG)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                if self.maze.is_wall(x, y):
                    color = COLOR_WALL
                else:
                    color = COLOR_FREE
                pygame.draw.rect(self.screen, color, rect)
        # Explored
        if explored:
            for (x, y) in explored:
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, COLOR_EXPLORED, rect)
        # Frontier
        if frontier:
            for (x, y) in frontier:
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, COLOR_FRONTIER, rect)
        # Path
        if path:
            for (x, y) in path:
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (0, 0, 200), rect)
        # Agent
        ax, ay = self.agent.agent_pos
        pygame.draw.circle(self.screen, COLOR_AGENT,
                           (ax*self.cell_size + self.cell_size//2,
                            ay*self.cell_size + self.cell_size//2),
                           self.cell_size//2)
        # Cheese
        cx, cy = self.maze.cheese
        pygame.draw.circle(self.screen, COLOR_CHEESE,
                           (cx*self.cell_size + self.cell_size//2,
                            cy*self.cell_size + self.cell_size//2),
                           self.cell_size//2)
        pygame.display.flip()

    def run(self, start_pos, strategy=None):
        self.agent = State(start_pos, self.maze)
        if strategy is None:
            strategy = select_initial_strategy(self.maze)
        history = []  # para heurística
        running = True
        paused = False
        path = []
        frontier = []
        explored = set()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_r:
                        self.maze.move_cheese()
                        self.agent = State(start_pos, self.maze)
                        history.clear()

            if not paused:
                # Ejecutar paso de búsqueda
                if strategy == 'astar':
                    path = astar(self.agent, manhattan)
                elif strategy == 'bfs':
                    path = bfs(self.agent)
                else:
                    path = dfs(self.agent)
                
                # Extraer fronteras y explorados si se quiere visualizar (opcional)
                # Aquí puedes descomponer según tu propia implementación
                explored = set()
                frontier = []

                # Historial para cambio de estrategia
                heur_val = manhattan(self.agent)
                history.append((len(history), heur_val))
                if should_switch_strategy(history):
                    strategy = 'bfs' if strategy == 'astar' else 'astar'
                    history.clear()

            self.draw(path, frontier, explored)
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()