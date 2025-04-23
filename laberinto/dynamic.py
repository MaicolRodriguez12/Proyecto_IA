# dynamic.py
import pygame
import sys
from .grid import Grid
from agent.Agent import Agent

# Colores y márgenes\
COLOR_FONDO = (255, 255, 255)
COLOR_PARED = (100, 100, 100)
MARGIN = 2

class Box:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = pygame.font.Font(None, 36).render(text, True, (0, 0, 0))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode
            self.txt_surface = pygame.font.Font(None, 36).render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        return int(self.text) if self.text.isdigit() else 0


def menu():
    pygame.init()
    screen = pygame.display.set_mode((500, 200))
    pygame.display.set_caption("Configurar Tablero")
    font = pygame.font.Font(None, 36)

    box_rows = Box(200, 50, 100, 40)
    box_cols = Box(200, 110, 100, 40)
    btn = pygame.Rect(180, 160, 140, 30)
    clock = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            box_rows.handle_event(e)
            box_cols.handle_event(e)
            if e.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(e.pos):
                r, c = box_rows.get_value(), box_cols.get_value()
                if r > 0 and c > 0:
                    return r, c

        screen.fill((240, 240, 240))
        screen.blit(font.render("Filas:", True, (0, 0, 0)), (50, 50))
        screen.blit(font.render("Columnas:", True, (0, 0, 0)), (50, 110))
        box_rows.draw(screen)
        box_cols.draw(screen)
        pygame.draw.rect(screen, (100, 200, 100), btn)
        screen.blit(font.render("Siguiente", True, (255, 255, 255)), (btn.x + 20, btn.y + 5))
        pygame.display.flip()
        clock.tick(30)


def setup_board(rows, cols):
    win_w, win_h = 800, 600
    pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption("Editar Tablero: arrastra ratón/queso, clic para muros, ENTER para iniciar")
    clock = pygame.time.Clock()
    lab = Grid(rows, cols)

    grid_w = win_w - 100
    grid_h = win_h - 50
    cell_size = min(grid_w // cols, grid_h // rows)
    offset_x = (win_w - cell_size * cols) // 2
    offset_y = (win_h - cell_size * rows) // 2

    img_agent = pygame.transform.scale(pygame.image.load("raton.png"), (cell_size-2*MARGIN, cell_size-2*MARGIN))
    img_goal  = pygame.transform.scale(pygame.image.load("queso.png"), (cell_size-2*MARGIN, cell_size-2*MARGIN))

    agent_pos = (0, 0)
    goal_pos = (rows-1, cols-1)
    rect_agent = img_agent.get_rect(topleft=(offset_x, offset_y))
    rect_goal  = img_goal.get_rect(topleft=(offset_x+(cols-1)*cell_size, offset_y+(rows-1)*cell_size))
    dragging = None

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if rect_agent.collidepoint(e.pos):
                    dragging = 'agent'
                elif rect_goal.collidepoint(e.pos):
                    dragging = 'goal'
                else:
                    mx, my = e.pos
                    c = (mx - offset_x) // cell_size
                    r = (my - offset_y) // cell_size
                    if 0 <= r < rows and 0 <= c < cols:
                        if lab.get_neighbors((r,c)):
                            lab.lock_cell((r,c))
                        else:
                            for d in ['top','right','bottom','left']:
                                lab.set_wall((r,c), d, False)
            elif e.type == pygame.MOUSEBUTTONUP:
                dragging = None
            elif e.type == pygame.MOUSEMOTION and dragging:
                mx, my = e.pos
                c = (mx - offset_x) // cell_size
                r = (my - offset_y) // cell_size
                if 0 <= r < rows and 0 <= c < cols:
                    if dragging == 'agent':
                        agent_pos = (r, c)
                        rect_agent.topleft = (offset_x + c*cell_size, offset_y + r*cell_size)
                    else:
                        goal_pos = (r, c)
                        rect_goal.topleft = (offset_x + c*cell_size, offset_y + r*cell_size)
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return lab, agent_pos, goal_pos, cell_size, offset_x, offset_y, img_agent, img_goal

        screen = pygame.display.get_surface()
        screen.fill(COLOR_FONDO)
        for r in range(rows):
            for c in range(cols):
                x = offset_x + c * cell_size + MARGIN
                y = offset_y + r * cell_size + MARGIN
                if not lab.get_neighbors((r,c)):
                    pygame.draw.rect(screen, COLOR_PARED, (x, y, cell_size-2*MARGIN, cell_size-2*MARGIN))
        screen.blit(img_agent, rect_agent)
        screen.blit(img_goal, rect_goal)
        # líneas horizontales corregidas
        for i in range(rows+1):
            pygame.draw.line(screen, (200,200,200), (offset_x, offset_y + i*cell_size),
                             (offset_x + cols*cell_size, offset_y + i*cell_size))
        # líneas verticales
        for j in range(cols+1):
            pygame.draw.line(screen, (200,200,200), (offset_x + j*cell_size, offset_y),
                             (offset_x + j*cell_size, offset_y + rows*cell_size))

        pygame.display.flip()
        clock.tick(60)


def juego():
    rows, cols = menu()
    lab, agent_pos, goal_pos, cell_size, off_x, off_y, img_agent, img_goal = setup_board(rows, cols)

    agent = Agent(lab, algorithm="A*")
    agent.find_path(agent_pos, goal_pos)
    if not agent.path:
        pygame.display.set_caption("No hay ruta al queso. Reinicia (ESC).")
    current = list(agent_pos)
    last = pygame.time.get_ticks()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
        now = pygame.time.get_ticks()
        if now - last >= 500 and agent.path:
            nxt = agent.get_next_move()
            if nxt:
                current = list(nxt)
            last = now

        screen = pygame.display.get_surface()
        screen.fill(COLOR_FONDO)
        for r in range(rows):
            for c in range(cols):
                x = off_x + c * cell_size + MARGIN
                y = off_y + r * cell_size + MARGIN
                if (r,c) == tuple(current):
                    screen.blit(img_agent, (x, y))
                elif (r,c) == goal_pos:
                    screen.blit(img_goal, (x, y))
                elif not lab.get_neighbors((r,c)):
                    pygame.draw.rect(screen, COLOR_PARED, (x, y, cell_size-2*MARGIN, cell_size-2*MARGIN))
        # líneas horizontales de simulación
        for i in range(rows+1):
            pygame.draw.line(screen, (200,200,200), (off_x, off_y + i*cell_size),
                             (off_x + cols*cell_size, off_y + i*cell_size))
        # líneas verticales de simulación
        for j in range(cols+1):
            pygame.draw.line(screen, (200,200,200), (off_x + j*cell_size, off_y),
                             (off_x + j*cell_size, off_y + rows*cell_size))

        if tuple(current) == goal_pos:
            font = pygame.font.Font(None, 72)
            text = font.render("¡Llegaste al queso!", True, (0, 128, 0))
            screen.blit(text, (off_x, 10))
            pygame.display.flip()
            pygame.time.delay(2000)
            break

        pygame.display.flip()
        pygame.time.delay(100)


def main():
    while True:
        juego()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
