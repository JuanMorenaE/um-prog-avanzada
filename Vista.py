import pygame

from Tablero import TOTAL_CASILLAS
from Utils import Color

# El tablero es el perímetro de una grilla de 10x10:
# 10 casillas de la columna izquierda + 9 de la fila superior
# + 9 de la columna derecha + 8 de la fila inferior = 36 casillas.
COLUMNAS = 10
FILAS = 10

TAM_CASILLA = 64
MARGEN = 40

ANCHO_VENTANA = COLUMNAS * TAM_CASILLA + MARGEN * 2
ALTO_VENTANA = FILAS * TAM_CASILLA + MARGEN * 2

COLOR_FONDO = (24, 26, 32)
COLOR_CASILLA = (238, 238, 230)
COLOR_CASILLA_ESPECIAL = (250, 214, 137)
COLOR_CASILLA_INICIO = (167, 226, 167)
COLOR_CASILLA_FINAL = (226, 167, 167)
COLOR_BORDE = (60, 62, 70)
COLOR_TEXTO = (40, 42, 48)

COLORES_FICHA = {
    Color.ROJO: (214, 48, 49),
    Color.VERDE: (0, 168, 89),
    Color.AZUL: (32, 99, 214),
    Color.AMARILLO: (240, 196, 25),
}


def coordenada_grilla(posicion):
    """Devuelve la (columna, fila) de la grilla para una casilla del tablero.

    La casilla 0 está abajo a la izquierda y el recorrido sube por la columna
    izquierda, sigue por la fila de arriba hacia la derecha, baja por la
    columna derecha y vuelve por la fila de abajo hasta la casilla 35, que
    queda al lado de la casilla 0.
    """
    posicion = posicion % TOTAL_CASILLAS

    if posicion < FILAS:                       # 0..9   columna izquierda, hacia arriba
        return 0, FILAS - 1 - posicion

    if posicion < FILAS + COLUMNAS - 1:        # 10..18 fila superior, hacia la derecha
        return posicion - (FILAS - 1), 0

    if posicion < FILAS * 2 + COLUMNAS - 2:    # 19..27 columna derecha, hacia abajo
        return COLUMNAS - 1, posicion - (FILAS + COLUMNAS - 2)

    return TOTAL_CASILLAS - posicion, FILAS - 1  # 28..35 fila inferior, hacia la izquierda


def rectangulo_casilla(posicion):
    columna, fila = coordenada_grilla(posicion)

    return pygame.Rect(
        MARGEN + columna * TAM_CASILLA,
        MARGEN + fila * TAM_CASILLA,
        TAM_CASILLA,
        TAM_CASILLA,
    )


class Vista:
    def __init__(self, tablero):
        pygame.init()

        self._tablero = tablero
        self._abierta = True
        self._pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Tablero")

        self._fuente_casilla = pygame.font.SysFont("consolas", 16)
        self._fuente_ficha = pygame.font.SysFont("consolas", 14, bold=True)

    def color_de_casilla(self, posicion):
        if posicion == 0:
            return COLOR_CASILLA_INICIO

        if posicion == TOTAL_CASILLAS - 1:
            return COLOR_CASILLA_FINAL

        if self._tablero.obtener_casilla_especial(posicion) is not None:
            return COLOR_CASILLA_ESPECIAL

        return COLOR_CASILLA

    def dibujar_casilla(self, posicion):
        rect = rectangulo_casilla(posicion)

        pygame.draw.rect(self._pantalla, self.color_de_casilla(posicion), rect, border_radius=6)
        pygame.draw.rect(self._pantalla, COLOR_BORDE, rect, width=2, border_radius=6)

        numero = self._fuente_casilla.render(f"{posicion:02}", True, COLOR_TEXTO)
        self._pantalla.blit(numero, (rect.x + 5, rect.y + 4))

    def dibujar_fichas(self, posicion):
        fichas = self._tablero._casillas[posicion]

        if not fichas:
            return

        rect = rectangulo_casilla(posicion)
        radio = 11
        centro_x = rect.centerx
        centro_y = rect.centery + 6

        # Las fichas apiladas se dibujan en fila para que se vean todas.
        ancho_total = (len(fichas) - 1) * (radio + 2)
        inicio_x = centro_x - ancho_total // 2

        for i, ficha in enumerate(fichas):
            centro = (inicio_x + i * (radio + 2), centro_y)

            pygame.draw.circle(self._pantalla, COLORES_FICHA[ficha._color], centro, radio)
            pygame.draw.circle(self._pantalla, COLOR_BORDE, centro, radio, width=2)

    def dibujar(self):
        # Sin esto la ventana queda "no responde" para el sistema operativo.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self._abierta = False

        if not self._abierta:
            return False

        self._pantalla.fill(COLOR_FONDO)

        for posicion in range(TOTAL_CASILLAS):
            self.dibujar_casilla(posicion)
            self.dibujar_fichas(posicion)

        pygame.display.flip()

        return True


if __name__ == "__main__":
    from Tablero import Tablero
    from Ficha import Ficha

    tablero = Tablero()

    # Fichas de ejemplo para ver el recorrido.
    for posicion, color in [(0, Color.ROJO), (5, Color.VERDE), (18, Color.AZUL), (35, Color.AMARILLO)]:
        tablero._casillas[posicion].append(Ficha(color, posicion))

    vista = Vista(tablero)

    reloj = pygame.time.Clock()
    while vista.dibujar():
        reloj.tick(30)

    pygame.quit()
