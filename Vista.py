import pygame

from Constantes import TOTAL_CASILLAS, CASILLA_FINAL
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
COLOR_CASILLA_ESPECIAL_POSITIVA = (249, 203, 156)
COLOR_CASILLA_ESPECIAL_NEGATIVA = (224, 102, 102)
COLOR_CASILLA_INICIO = (0, 255, 0)
COLOR_CASILLA_FINAL = (201, 218, 248)
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
    def __init__(self, juego):
        pygame.init()

        # La vista necesita el juego y no solo el tablero: el tablero tiene las
        # fichas, pero las casillas especiales las maneja Juego.
        self._juego = juego
        self._tablero = juego.tablero
        self._abierta = True
        self._pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Tablero")

        self._fuente_casilla = pygame.font.SysFont("consolas", 16)
        self._fuente_ficha = pygame.font.SysFont("consolas", 14, bold=True)

    def color_de_casilla(self, posicion):
        if posicion == 0:
            return COLOR_CASILLA_INICIO

        if posicion == CASILLA_FINAL:
            return COLOR_CASILLA_FINAL

        efecto = self._juego.obtener_casilla_especial(posicion)

        if efecto is not None:
            # Las casillas P (premio) son positivas y las C (castigo) negativas,
            # así que se distinguen por color según el nombre del efecto.
            if self.es_casilla_positiva(efecto):
                return COLOR_CASILLA_ESPECIAL_POSITIVA

            return COLOR_CASILLA_ESPECIAL_NEGATIVA

        return COLOR_CASILLA

    @staticmethod
    def es_casilla_positiva(efecto):
        return efecto.__name__.startswith("efecto_P")

    @staticmethod
    def etiqueta_casilla(efecto):
        return efecto.__name__.removeprefix("efecto_")

    def dibujar_casilla(self, posicion):
        rect = rectangulo_casilla(posicion)

        pygame.draw.rect(self._pantalla, self.color_de_casilla(posicion), rect, border_radius=6)
        pygame.draw.rect(self._pantalla, COLOR_BORDE, rect, width=2, border_radius=6)

        numero = self._fuente_casilla.render(f"{posicion+1:02}", True, COLOR_TEXTO)
        self._pantalla.blit(numero, (rect.x + 5, rect.y + 4))

        efecto = self._juego.obtener_casilla_especial(posicion)

        if efecto is not None:
            etiqueta = self._fuente_casilla.render(self.etiqueta_casilla(efecto), True, COLOR_TEXTO)
            self._pantalla.blit(etiqueta, (rect.right - etiqueta.get_width() - 5, rect.y + 4))

    def dibujar_fichas(self, posicion):
        fichas = self._tablero.casillas[posicion]

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

            pygame.draw.circle(self._pantalla, COLORES_FICHA[ficha.color], centro, radio)
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