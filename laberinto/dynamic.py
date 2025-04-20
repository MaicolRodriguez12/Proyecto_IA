import pygame
import sys
import random
from grid import Grid  

TAM_CELDA = 60
MARGEN = 7
COLOR_FONDO = (255, 255, 255)
COLOR_AGENT = (144, 238, 144)
COLOR_OBJETIVO = (255, 255, 102)
COLOR_PARED = (100, 100, 100)


class Box:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = pygame.font.Font(None, 36).render(text, True, self.color)
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
    pantalla = pygame.display.set_mode((500, 400))
    pygame.display.set_caption("LABERINTO DINÁMICO")
    fuente = pygame.font.Font(None, 36)

    input_rows = Box(200, 50, 100, 40)
    input_columns = Box(200, 120, 100, 40)
    input_obstaculos = Box(200, 190, 100, 40)

    input_boxes = [input_rows, input_columns, input_obstaculos]

    boton_rect = pygame.Rect(180, 270, 140, 50)
    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and boton_rect.collidepoint(event.pos):
                rows = input_rows.get_value()
                columns = input_columns.get_value() 
                obstaculos = input_obstaculos.get_value()
                total_disponibles = rows * columns - 2

                if rows > 0 and columns > 0 and 0 <= obstaculos <= total_disponibles:
                    ejecutando = False
                    return rows, columns, obstaculos

        pantalla.fill((240, 240, 240))
        pantalla.blit(fuente.render("Filas:", True, (0, 0, 0)), (40, 60))
        pantalla.blit(fuente.render("Columnas:", True, (0, 0, 0)), (40, 130))
        pantalla.blit(fuente.render("Obstáculos:", True, (0, 0, 0)), (40, 200))

        for box in input_boxes:
            box.draw(pantalla)

        pygame.draw.rect(pantalla, (100, 200, 100), boton_rect)
        pantalla.blit(fuente.render("Iniciar", True, (255, 255, 255)), (boton_rect.x + 33, boton_rect.y + 13))

        pygame.display.flip()
        reloj.tick(30)

rows, columns, obstaculos = menu()


lab = Grid(rows, columns)

total_celdas = [(r, c) for r in range(rows) for c in range(columns)]

# Elegir 1 agente, 1 objetivo y 5 paredes (sin repetidos)
aleatorias = random.sample(total_celdas, 2 + obstaculos)  # agente, objetivo + obstáculos
agente_pos = aleatorias[0]
objetivo = aleatorias[1]
paredes = aleatorias[2:]

# Asignar posición inicial del agente
agente = list(agente_pos)

# Bloquear celdas
for p in paredes:
    lab.lock_cell(p)


# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((columns * TAM_CELDA, rows * TAM_CELDA))
pygame.display.set_caption("Laberinto Dinámico")
reloj = pygame.time.Clock()

def mover_agente(dx, dy):
    nueva_pos = (agente[0] + dy, agente[1] + dx)

    # Validar que esté dentro del laberinto
    if 0 <= nueva_pos[0] < rows and 0 <= nueva_pos[1] < columns:
        # Validar que hay conexión en el grafo
        if nueva_pos in lab.show_neighbors(tuple(agente)):
            print(f"Moviendo agente a {nueva_pos}")
            agente[0] += dy
            agente[1] += dx
        else:
            print(f"Movimiento bloqueado hacia {nueva_pos}")
    else:
        print(f"Movimiento fuera de límites hacia {nueva_pos}")

def dibujar_rejilla(surface):
    for fila in range(rows + 1):
        y = fila * TAM_CELDA
        pygame.draw.line(surface, (200, 200, 200), (0, y), (columns * TAM_CELDA, y), 1)
    for col in range(columns + 1):
        x = col * TAM_CELDA
        pygame.draw.line(surface, (200, 200, 200), (x, 0), (x, rows * TAM_CELDA), 1)


ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                mover_agente(0, -1)
            elif evento.key == pygame.K_DOWN:
                mover_agente(0, 1)
            elif evento.key == pygame.K_LEFT:
                mover_agente(-1, 0)
            elif evento.key == pygame.K_RIGHT:
                mover_agente(1, 0)

    ventana.fill(COLOR_FONDO)

    # Dibuja las celdas
    for fila in range(rows):
        for col in range(columns):
            celda = (fila, col)
            color = COLOR_FONDO

            if celda == tuple(agente):
                color = COLOR_AGENT
            elif celda == objetivo:
                color = COLOR_OBJETIVO
            elif len(lab.show_neighbors(celda)) == 0:
                color = COLOR_PARED

            pygame.draw.rect(ventana, color,
                             (col * TAM_CELDA + MARGEN,
                              fila * TAM_CELDA + MARGEN,
                              TAM_CELDA - 2 * MARGEN,
                              TAM_CELDA - 2 * MARGEN))

    # Dibuja la rejilla encima
    dibujar_rejilla(ventana)

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
sys.exit()
