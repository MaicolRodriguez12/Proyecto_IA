import argparse
from proyecto_ia.maze import Maze
from proyecto_ia.gui import GUI


def parse_args():
    parser = argparse.ArgumentParser(description="Agente en Laberinto Dinámico")
    parser.add_argument('--width', type=int, default=20, help='Ancho del laberinto')
    parser.add_argument('--height', type=int, default=20, help='Alto del laberinto')
    parser.add_argument('--obstacle_prob', type=float, default=0.2, help='Probabilidad de pared inicial')
    parser.add_argument('--strategy', type=str, choices=['bfs', 'dfs', 'astar'], help='Estrategia inicial (override)')
    parser.add_argument('--cell_size', type=int, default=20, help='Tamaño de cada celda en la GUI')
    return parser.parse_args()


def main():
    args = parse_args()
    maze = Maze(args.width, args.height, args.obstacle_prob)
    start = maze.random_empty_cell()


    gui = GUI(maze, cell_size=args.cell_size)
    gui.run(start, strategy=args.strategy)


if __name__ == '__main__':
    main()
