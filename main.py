from laberinto.Box import menu, setup_board, COLOR_FONDO, COLOR_PARED, MARGIN
from agent.AdaptiveAgent import AdaptiveAgent
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
    for _ in range(cantidad):
        while True:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            cell = laberinto.get_cell((r, c))
            if cell.trap_type is not None:
                cell.trap_type = None
                break

def juego():
    rows, cols, modo = menu()
    lab, ag, go, cs, ox, oy, img_a, img_g, img_rat, img_cat = setup_board(rows, cols, modo)
    cur = list(ag)
    last = pygame.time.get_ticks()
    traversed_cells = set()

    agent = AdaptiveAgent(lab, ag, go, initial_algorithm="A*")
    agent.select_algorithm()
    agent.plan_path()

    if not agent.agent.path:
        sfc = pygame.display.get_surface()
        sfc.fill(COLOR_FONDO)
        f = pygame.font.Font(None, 42)
        t = f.render('No hay camino, ESC para reiniciar', True, (255, 0, 0))
        sfc.blit(t, (ox, 10))
        pygame.display.flip()
        pygame.time.delay(5000)

    last_explored_cell = None
    intento_hecho = False
    contador_iteraciones = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                return

        now = pygame.time.get_ticks()

        if contador_iteraciones % 5 == 0:
            go = mover_queso(lab, rows, cols, go)
            agent.start = tuple(cur)
            agent.goal = go
            agent.select_algorithm()  # Selecciona el algoritmo adecuado
            agent.plan_path()  # Vuelve a planificar el camino con el nuevo algoritmo

        if contador_iteraciones % 3 == 0:
            modificar_obstaculos(lab, rows, cols, cantidad=1)

        if contador_iteraciones % 5 == 0:
            eliminar_obstaculos(lab, rows, cols, cantidad=1)

        if now - last >= 100:
            nxt = agent.get_next_move()
            cur = list(nxt) if nxt else cur
            traversed_cells.add(tuple(cur))

            if nxt:
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
        pygame.time.delay(500)

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
