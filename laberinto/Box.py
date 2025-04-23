# Box.py
import pygame
import sys
from .grid import Grid
import random

#importar las imágenes de los gatos y ratoneras
gato = "sources/gato.png"
ratonera = "sources/ratonera.png"
queso = "sources/queso.png"
raton = "sources/raton.png"


# Definir la clase Grid

# Colores y márgenes\
COLOR_FONDO = (255, 255, 255)
COLOR_PARED = (100, 100, 100)
COLOR_TRAP = (255, 100, 100)
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
    screen = pygame.display.set_mode((500, 350))
    pygame.display.set_caption("Configurar Tablero")
    font = pygame.font.Font(None, 36)

    box_rows = Box(200, 50, 100, 40)
    box_cols = Box(200, 110, 100, 40)
    btn = pygame.Rect(180, 270, 110, 30)

    manual_button = pygame.Rect(50, 210, 140, 30)
    random_button = pygame.Rect(260, 210, 140, 30)
    modo = "manual"

    clock = pygame.time.Clock()
  
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            box_rows.handle_event(e)
            box_cols.handle_event(e)
            if e.type == pygame.MOUSEBUTTONDOWN:
                if manual_button.collidepoint(e.pos):
                    modo = "manual"
                elif random_button.collidepoint(e.pos):
                    modo = "random"
                elif btn.collidepoint(e.pos):
                    r, c = box_rows.get_value(), box_cols.get_value()
                    if r > 0 and c > 0:
                        return r, c, modo

        screen.fill((240, 240, 240))
        screen.blit(font.render("Filas:", True, (0, 0, 0)), (50, 50))
        screen.blit(font.render("Columnas:", True, (0, 0, 0)), (50, 110))
        screen.blit(font.render("Modo obstáculos:", True, (0, 0, 0)), (50, 170))
        box_rows.draw(screen)
        box_cols.draw(screen)

        pygame.draw.rect(screen, (0, 150, 255) if modo == "manual" else (200, 200, 200), manual_button)
        pygame.draw.rect(screen, (0, 150, 255) if modo == "random" else (200, 200, 200), random_button)
        screen.blit(font.render("Manual", True, (0, 0, 0)), (manual_button.x + 19, manual_button.y + 2))
        screen.blit(font.render("Aleatorio", True, (0, 0, 0)), (random_button.x + 19, random_button.y + 2))

        pygame.draw.rect(screen, (100, 200, 100), btn)
        screen.blit(font.render("Jugar", True, (255, 255, 255)), (btn.x + 20, btn.y + 3))
        pygame.display.flip()
        clock.tick(30)


def setup_board(rows, cols, modo):
    win = (500,500)
    pygame.display.set_mode(win)
    pygame.display.set_caption('Editar: clic muros, SHIFT+clic ratonera, CTRL+clic gato, arrastrar, ENTER')
    clk = pygame.time.Clock()
    lab = Grid(rows, cols)
    cell_size=min((win[0]-100)//cols,(win[1]-50)//rows)
    ox=(win[0]-cell_size*cols)//2; oy=(win[1]-cell_size*rows)//2
    img_agent=pygame.transform.scale(pygame.image.load(raton),(cell_size-2*MARGIN,cell_size-2*MARGIN))
    img_goal=pygame.transform.scale(pygame.image.load(queso),(cell_size-2*MARGIN,cell_size-2*MARGIN))
    img_rat=pygame.transform.scale(pygame.image.load(ratonera),(cell_size-2*MARGIN,cell_size-2*MARGIN))
    img_cat=pygame.transform.scale(pygame.image.load(gato),(cell_size-2*MARGIN,cell_size-2*MARGIN))
    agent=(0,0); goal=(rows-1,cols-1)
    rect_a=img_agent.get_rect(topleft=(ox,oy)); rect_g=img_goal.get_rect(topleft=(ox+(cols-1)*cell_size,oy+(rows-1)*cell_size))
    drag=None

    if modo == 'random':
        for _ in range((rows * cols) // 6):  # Ajusta densidad como quieras
            r, c = random.randint(0, rows-1), random.randint(0, cols-1)
            if (r, c) not in [(0,0), (rows-1, cols-1)]:
                if random.random() < 0.3:
                    lab.set_trap((r,c), 'ratonera')
                elif random.random() < 0.6:
                    lab.set_trap((r,c), 'gato')
                else:
                    lab.lock_cell((r,c))
        return lab, agent, goal, cell_size, ox, oy, img_agent, img_goal, img_rat, img_cat


    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                mods=pygame.key.get_mods(); s=mods&pygame.KMOD_SHIFT; ctrl=mods&pygame.KMOD_CTRL
                if rect_a.collidepoint(e.pos): drag='agent'
                elif rect_g.collidepoint(e.pos): drag='goal'
                else:
                    mx,my=e.pos; c=(mx-ox)//cell_size; r=(my-oy)//cell_size
                    if 0<=r<rows and 0<=c<cols:
                        if s:
                            lab.set_trap((r,c),'ratonera')
                        elif ctrl:
                            lab.set_trap((r,c),'gato')
                        else:
                            if lab.get_neighbors((r,c)): lab.lock_cell((r,c))
                            else: [lab.set_wall((r,c),d,False) for d in ['top','right','bottom','left']]
            if e.type==pygame.MOUSEBUTTONUP: drag=None
            if e.type==pygame.MOUSEMOTION and drag:
                mx,my=e.pos; c=(mx-ox)//cell_size; r=(my-oy)//cell_size
                if 0<=r<rows and 0<=c<cols:
                    if drag=='agent': agent=(r,c); rect_a.topleft=(ox+c*cell_size,oy+r*cell_size)
                    else: goal=(r,c); rect_g.topleft=(ox+c*cell_size,oy+r*cell_size)
            if e.type==pygame.KEYDOWN and e.key==pygame.K_RETURN: return lab,agent,goal,cell_size,ox,oy,img_agent,img_goal,img_rat,img_cat
        sfc=pygame.display.get_surface(); sfc.fill(COLOR_FONDO)
        for r in range(rows):
            for c in range(cols):
                x=ox+c*cell_size+MARGIN; y=oy+r*cell_size+MARGIN; cell=lab.get_cell((r,c))
                if cell.trap_type=='ratonera': sfc.blit(img_rat,(x,y))
                elif cell.trap_type=='gato':    sfc.blit(img_cat,(x,y))
                elif not lab.get_neighbors((r,c)): pygame.draw.rect(sfc,COLOR_PARED,(x,y,cell_size-2*MARGIN,cell_size-2*MARGIN))
        sfc.blit(img_agent,rect_a); sfc.blit(img_goal,rect_g)
        for i in range(rows+1): pygame.draw.line(sfc,(200,200,200),(ox,oy+i*cell_size),(ox+cols*cell_size,oy+i*cell_size))
        for j in range(cols+1): pygame.draw.line(sfc,(200,200,200),(ox+j*cell_size,oy),(ox+j*cell_size,oy+rows*cell_size))
        pygame.display.flip(); clk.tick(60)

