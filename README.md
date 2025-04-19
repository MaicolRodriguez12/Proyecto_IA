## Proyecto IA: Agente de Navegación en Laberinto Dinámico

Este repositorio contiene la implementación de un agente inteligente capaz de navegar en un laberinto dinámico utilizando técnicas de búsqueda (BFS, DFS y A*), con capacidad de adaptar su estrategia en tiempo de ejecución ante cambios en el entorno. La interfaz gráfica se realiza con Pygame.
## Descripción del Proyecto

Este proyecto forma parte de la asignatura de Inteligencia Artificial (2025-1). El objetivo es diseñar y desarrollar un agente que pueda encontrar rutas hacia un objetivo ("queso") en un laberinto cuyas paredes, obstáculos y meta pueden cambiar durante la ejecución. El agente podrá alternar entre BFS, DFS y A* según las necesidades del entorno.

## Características Principales

- Laberinto dinámico con cambios en tiempo real (muros que aparecen/desaparecen, queso que se mueve).  
- Agente con tres técnicas de búsqueda implementadas: BFS, DFS y A*.  
- Mecanismo de decisión para cambiar de algoritmo durante la ejecución.  
- Interfaz gráfica interactiva desarrollada en Pygame.  
- Tableros configurables en tamaño y estado inicial.  

## Requisitos

- Python 3.8 o superior  
- Librerías:
  - `pygame`
  - `networkx`
  - `numpy`
