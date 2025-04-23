import pygame
import sys
import random
from .grid import Grid 
from agent.Agent import Agent

TAM_CELDA = 60
MARGEN = 4
COLOR_FONDO = (255, 255, 255)
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

    while True:
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


def juego():
    rows, columns, obstaculos = menu()
    lab = Grid(rows, columns)
    total_celdas = [(r, c) for r in range(rows) for c in range(columns)]
    aleatorias = random.sample(total_celdas, 2 + obstaculos)
    agente_pos, objetivo = aleatorias[0], aleatorias[1]
    for p in aleatorias[2:]:
        lab.lock_cell(p)

    # Instanciar agente y calcular ruta
    agent = Agent(lab, algorithm="A*")
    agent.find_path(agente_pos, objetivo)
    agente = list(agente_pos)
    recorrido = [tuple(agente)]  # Guardar posiciones visitadas

    pygame.init()
    ventana = pygame.display.set_mode((columns * TAM_CELDA, rows * TAM_CELDA))
    pygame.display.set_caption("Laberinto Dinámico")
    reloj = pygame.time.Clock()
    img_agent = pygame.transform.scale(pygame.image.load("raton.png"), (TAM_CELDA - 2*MARGEN, TAM_CELDA - 2*MARGEN))
    img_goal = pygame.transform.scale(pygame.image.load("queso.png"), (TAM_CELDA - 2*MARGEN, TAM_CELDA - 2*MARGEN))
    tiempo_ultimo_movimiento = 0
    intervalo_movimiento = 500

    while True:
        tiempo_actual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return

        if tiempo_actual - tiempo_ultimo_movimiento >= intervalo_movimiento:
            next_pos = agent.get_next_move()
            if next_pos is not None:
                agente[0], agente[1] = next_pos
                recorrido.append(tuple(agente))
                tiempo_ultimo_movimiento = tiempo_actual

        # Dibujado
        ventana.fill(COLOR_FONDO)
        for fila in range(rows):
            for col in range(columns):
                x, y = col*TAM_CELDA+MARGEN, fila*TAM_CELDA+MARGEN
                celda = (fila, col)
                if celda == tuple(agente):
                    ventana.blit(img_agent, (x, y))
                elif celda == objetivo:
                    ventana.blit(img_goal, (x, y))
                elif not lab.get_neighbors(celda):
                    pygame.draw.rect(ventana, COLOR_PARED, (x, y, TAM_CELDA-2*MARGEN, TAM_CELDA-2*MARGEN))
                elif celda in recorrido:
                    pygame.draw.rect(ventana, (173, 216, 230), (x, y, TAM_CELDA-2*MARGEN, TAM_CELDA-2*MARGEN))  # celeste

        for f in range(rows+1):
            pygame.draw.line(ventana, (200,200,200), (0,f*TAM_CELDA),(columns*TAM_CELDA,f*TAM_CELDA),1)
        for c in range(columns+1):
            pygame.draw.line(ventana, (200,200,200), (c*TAM_CELDA,0),(c*TAM_CELDA,rows*TAM_CELDA),1)

        if tuple(agente) == objetivo:
            fuente = pygame.font.Font(None,72)
            texto = fuente.render("¡Ganaste!", True, (0,128,0))
            ventana.blit(texto, (ventana.get_width()//2 - texto.get_width()//2,
                                 ventana.get_height()//2 - texto.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(2000)

        pygame.display.flip()
        reloj.tick(60)


def main():
    while True:
        juego()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
