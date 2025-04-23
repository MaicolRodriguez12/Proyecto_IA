from laberinto.Box import menu, setup_board, COLOR_FONDO, COLOR_PARED, MARGIN
from agent.Agent import Agent
import pygame
import sys

def juego():
    rows, cols, modo = menu()
    lab, ag, go, cs, ox, oy, img_a, img_g, img_rat, img_cat = setup_board(rows, cols, modo)

    agent = Agent(lab, 'BFS')
    agent.find_path(ag, go)

    cur = list(ag)
    last = pygame.time.get_ticks()
    traversed_cells = set()
    intento_hecho = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                return

        now = pygame.time.get_ticks()

        if now - last >= 500:
            nxt = agent.get_next_move()  ### ← Usamos siempre get_next_move (exploración o camino)
            if nxt:
                cur = list(nxt)
                traversed_cells.add(tuple(cur))
                intento_hecho = True
            else:
                # Si no hay más movimientos, mostrar mensaje de fallo solo si no llegó al queso
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

        # Dibujar celdas y objetos
        for r in range(rows):
            for c in range(cols):
                x = ox + c * cs + MARGIN
                y = oy + r * cs + MARGIN

                if (r, c) == tuple(cur):
                    sfc.blit(img_a, (x, y))
                elif (r, c) == go:
                    sfc.blit(img_g, (x, y))
                elif lab.get_cell((r, c)).trap_type == 'ratonera':
                    sfc.blit(img_rat, (x, y))
                elif lab.get_cell((r, c)).trap_type == 'gato':
                    sfc.blit(img_cat, (x, y))
                elif not lab.get_neighbors((r, c)):
                    pygame.draw.rect(sfc, COLOR_PARED, (x, y, cs - 2 * MARGIN, cs - 2 * MARGIN))

                # Celdas exploradas
                if (r, c) in traversed_cells and (r, c) != tuple(cur) and (r, c) != tuple(ag):
                    traversed_cell = lab.get_cell((r, c))
                    if isinstance(traversed_cell.traversed_color, tuple) and len(traversed_cell.traversed_color) == 3:
                        pygame.draw.rect(sfc, traversed_cell.traversed_color, (x, y, cs - 2 * MARGIN, cs - 2 * MARGIN))

        # Dibujar las líneas del tablero
        for i in range(rows + 1):
            pygame.draw.line(sfc, (200, 200, 200), (ox, oy + i * cs), (ox + cols * cs, oy + i * cs))
        for j in range(cols + 1):
            pygame.draw.line(sfc, (200, 200, 200), (ox + j * cs, oy), (ox + j * cs, oy + rows * cs))

        # Mostrar información del agente
        font = pygame.font.Font(None, 36)
        texto_pasos = font.render(f"Pasos: {agent.total_steps}", True, (0, 0, 0))
        texto_costo = font.render(f"Costo total: {agent.total_cost}", True, (0, 0, 0))
        texto_algoritmo = font.render(f"Algoritmo: {agent.algorithm}", True, (0, 0, 0))
        sfc.blit(texto_algoritmo, (ox + 400, oy + rows * cs + 10))
        sfc.blit(texto_pasos, (ox, oy + rows * cs + 10))
        sfc.blit(texto_costo, (ox + 200, oy + rows * cs + 10))

        pygame.display.flip()
        pygame.time.delay(100)

        # Llegó al queso
        if tuple(cur) == go:
            f = pygame.font.Font(None, 42)
            t = f.render('¡Amigo el ratón del queso!', True, (0, 128, 0))
            sfc.blit(t, (ox, 10))
            pygame.display.flip()
            pygame.time.delay(5000)
            break

def main():
    while True:
        juego()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
