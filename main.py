from laberinto.Box import menu, setup_board, COLOR_FONDO, COLOR_PARED, MARGIN
from agent.Agent import Agent
import pygame
import sys
import random

def mover_queso(laberinto, rows, cols, go):
    while True:
        nueva_pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        if laberinto.get_cell(nueva_pos).trap_type is None:
            return nueva_pos

def modificar_obstaculos(laberinto, rows, cols, cantidad=1):
    for _ in range(cantidad):
        while True:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            cell = laberinto.get_cell((r, c))
            if cell.trap_type is None:
                tipo_obstaculo = random.choice(['ratonera', 'gato'])
                cell.trap_type = tipo_obstaculo
                break

def eliminar_obstaculos(laberinto, rows, cols, cantidad=1):
    """Función que elimina obstáculos aleatorios del laberinto."""
    for _ in range(cantidad):
        while True:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            cell = laberinto.get_cell((r, c))
            if cell.trap_type is not None:  # Solo elimina si hay un obstáculo
                cell.trap_type = None  # Elimina el obstáculo
                break

def juego():
    rows, cols, modo = menu()
    lab, ag, go, cs, ox, oy, img_a, img_g, img_rat, img_cat = setup_board(rows, cols, modo)
    cur = list(ag)
    last = pygame.time.get_ticks()
    
    traversed_cells = set()  # Set to store the cells traversed during the search
    
    agent = Agent(lab, algorithm='A*')
    agent.find_path(ag, go)
    #agent.find_best_path(ag, go)

    if not agent.path: 
        sfc = pygame.display.get_surface()
        sfc.fill(COLOR_FONDO)
        f = pygame.font.Font(None, 42)
        t = f.render('No hay camino, ESC para reiniciar', True, (255, 0, 0))
        sfc.blit(t, (ox, 10))
        pygame.display.flip()
        pygame.time.delay(5000)



    cur = list(ag)
    last = pygame.time.get_ticks()
    traversed_cells = set()
    last_explored_cell = None
    intento_hecho = False
    contador_iteraciones = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                return

        now = pygame.time.get_ticks()

        # Mover el queso cada 10 iteraciones
        if contador_iteraciones % 25 == 0:
            go = mover_queso(lab, rows, cols, go)
            agent.find_path(tuple(cur), go)

        # Modificar los obstáculos cada 10 iteraciones
        if contador_iteraciones % 10 == 0:
            modificar_obstaculos(lab, rows, cols, cantidad=1)

        # Eliminar obstáculos cada 50 iteraciones
        if contador_iteraciones % 30 == 0:
            eliminar_obstaculos(lab, rows, cols, cantidad=1)

        # Reducir la frecuencia de actualización para que el ratón se mueva más rápido
        if now - last >= 100:  # Reduce de 500 a 100 milisegundos (o incluso menos)
            nxt = agent.get_next_move()

            cur = list(nxt) if nxt else cur
            traversed_cells.add(tuple(cur))  

            if nxt:
                cur = list(nxt)
                traversed_cells.add(tuple(cur))
                last_explored_cell = tuple(cur)
                intento_hecho = True
            else:
                if intento_hecho and tuple(cur) != go:
                    sfc = pygame.display.get_surface()
                    f = pygame.font.Font(None, 42)
                    t = f.render('No hay camino, ESC para reiniciar', True, (255, 0, 0))
                    sfc.blit(t, (ox, 10))
                    pygame.display.flip()
                    pygame.time.delay(5000)
                    break
            last = now

        sfc = pygame.display.get_surface()
        sfc.fill(COLOR_FONDO)

        # Pintar última celda explorada primero (si no es donde está el ratón)
        if last_explored_cell and tuple(last_explored_cell) != tuple(cur):
            r, c = last_explored_cell
            x = ox + c * cs + MARGIN
            y = oy + r * cs + MARGIN
            pygame.draw.rect(sfc, (255, 165, 0), (x, y, cs - 2 * MARGIN, cs - 2 * MARGIN))

        for r in range(rows):
            for c in range(cols):
                x = ox + c * cs + MARGIN
                y = oy + r * cs + MARGIN
                pos = (r, c)

                if pos == tuple(cur):
                    sfc.blit(img_a, (x, y))
                elif pos == go:
                    sfc.blit(img_g, (x, y))
                elif lab.get_cell(pos).trap_type == 'ratonera':
                    sfc.blit(img_rat, (x, y))
                elif lab.get_cell(pos).trap_type == 'gato':
                    sfc.blit(img_cat, (x, y))
                elif not lab.get_neighbors(pos):
                    pygame.draw.rect(sfc, COLOR_PARED, (x, y, cs - 2 * MARGIN, cs - 2 * MARGIN))

                if pos in traversed_cells and pos != tuple(cur) and pos != tuple(ag):
                    cell = lab.get_cell(pos)
                    if isinstance(cell.traversed_color, tuple) and len(cell.traversed_color) == 3:
                        pygame.draw.rect(sfc, cell.traversed_color, (x, y, cs - 2 * MARGIN, cs - 2 * MARGIN))

        for i in range(rows + 1):
            pygame.draw.line(sfc, (200, 200, 200), (ox, oy + i * cs), (ox + cols * cs, oy + i * cs))
        for j in range(cols + 1):
            pygame.draw.line(sfc, (200, 200, 200), (ox + j * cs, oy), (ox + j * cs, oy + rows * cs))

        font = pygame.font.Font(None, 36)
        texto_pasos = font.render(f"Pasos: {agent.total_steps}", True, (0, 0, 0))
        texto_costo = font.render(f"Costo total: {agent.total_cost}", True, (0, 0, 0))
        texto_algoritmo = font.render(f"Algoritmo: {agent.algorithm}", True, (0, 0, 0))
        sfc.blit(texto_algoritmo, (ox + 400, oy + rows * cs + 10))
        sfc.blit(texto_pasos, (ox, oy + rows * cs + 10))
        sfc.blit(texto_costo, (ox + 200, oy + rows * cs + 10))

        pygame.display.flip()
        pygame.time.delay(20)  # Se reduce el delay a 20 para un movimiento más rápido

        if tuple(cur) == go:
            f = pygame.font.Font(None, 42)
            t = f.render('¡Amigo el ratón del queso!', True, (0, 128, 0))
            sfc.blit(t, (ox, 10))
            pygame.display.flip()
            pygame.time.delay(5000)
            break

        contador_iteraciones += 1

def main():
    while True:
        juego()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
