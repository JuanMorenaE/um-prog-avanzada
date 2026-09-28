import os
import pygame

if os.name == "nt":
    import msvcrt

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
COLOR_CASILLA_ESPECIAL_POSITIVA = (240, 185, 95)
COLOR_CASILLA_ESPECIAL_NEGATIVA = (205, 95, 95)
COLOR_CASILLA_INICIO = (105, 190, 120)
COLOR_CASILLA_FINAL = (105, 150, 220)
COLOR_BORDE = (60, 62, 70)
COLOR_TEXTO = (40, 42, 48)
COLOR_PANEL = (35, 38, 46)
COLOR_BORDE_PANEL = (78, 82, 94)
COLOR_TEXTO_PANEL = (235, 237, 242)
COLOR_TEXTO_SECUNDARIO = (170, 175, 188)

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
        # La vista necesita el juego y no solo el tablero: el tablero tiene las
        # fichas, pero las casillas especiales las maneja Juego.
        self._juego = juego
        self._tablero = juego.tablero
        self._abierta = False
        self._pantalla = None
        self._fuente_casilla = None
        self._fuente_ficha = None
        self._fuente_titulo = None
        self._fuente_panel = None
        self._fuente_dado = None
        self._jugador_actual = None
        self._ultimo_dado = None
        self._mensaje = "Esperando el primer turno"

    def iniciar(self):
        if self._abierta:
            return

        pygame.init()
        self._abierta = True
        self._pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Tablero")

        self._fuente_casilla = pygame.font.SysFont("consolas", 16)
        self._fuente_ficha = pygame.font.SysFont("consolas", 14, bold=True)
        self._fuente_titulo = pygame.font.SysFont("consolas", 28, bold=True)
        self._fuente_panel = pygame.font.SysFont("consolas", 20)
        self._fuente_dado = pygame.font.SysFont("consolas", 42, bold=True)

    def establecer_turno(self, jugador):
        self._jugador_actual = jugador
        self._ultimo_dado = None
        self._mensaje = f"Turno de {jugador.nombre}"

    def mostrar_dado(self, dado):
        self._ultimo_dado = dado
        self._mensaje = f"{self._jugador_actual.nombre} obtuvo {dado}"

    def mostrar_mensaje(self, mensaje):
        self._mensaje = mensaje

    def mostrar_ganador(self, jugador):
        reloj = pygame.time.Clock()
        fuente_ganador = pygame.font.SysFont("consolas", 54, bold=True)
        fuente_nombre = pygame.font.SysFont("consolas", 42, bold=True)
        fuente_indicacion = pygame.font.SysFont("consolas", 18)
        color_jugador = COLORES_FICHA[jugador.color]

        while self._abierta:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self._abierta = False
                elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self._abierta = False

            self._pantalla.fill(COLOR_FONDO)

            # Confeti decorativo alrededor del mensaje central.
            colores_confeti = list(COLORES_FICHA.values()) + [
                COLOR_CASILLA_ESPECIAL_POSITIVA,
                COLOR_TEXTO_PANEL,
            ]
            for indice in range(42):
                x = (indice * 83 + 35) % ANCHO_VENTANA
                y = (indice * 47 + 25) % ALTO_VENTANA
                color = colores_confeti[indice % len(colores_confeti)]
                pygame.draw.rect(self._pantalla, color, (x, y, 9, 18), border_radius=3)

            panel = pygame.Rect(95, 175, ANCHO_VENTANA - 190, ALTO_VENTANA - 350)
            pygame.draw.rect(self._pantalla, COLOR_PANEL, panel, border_radius=24)
            pygame.draw.rect(self._pantalla, color_jugador, panel, width=5, border_radius=24)

            titulo = fuente_ganador.render("¡GANADOR!", True, COLOR_CASILLA_ESPECIAL_POSITIVA)
            nombre = fuente_nombre.render(jugador.nombre.upper(), True, color_jugador)
            detalle = self._fuente_panel.render(
                f"Color: {jugador.color.name}", True, COLOR_TEXTO_PANEL
            )
            indicacion = fuente_indicacion.render(
                "Presioná ENTER o ESC para salir", True, COLOR_TEXTO_SECUNDARIO
            )

            self._pantalla.blit(titulo, (panel.centerx - titulo.get_width() // 2, panel.y + 55))
            self._pantalla.blit(nombre, (panel.centerx - nombre.get_width() // 2, panel.y + 145))
            self._pantalla.blit(detalle, (panel.centerx - detalle.get_width() // 2, panel.y + 215))
            self._pantalla.blit(
                indicacion,
                (panel.centerx - indicacion.get_width() // 2, panel.bottom - 55),
            )

            pygame.display.flip()
            reloj.tick(30)

        pygame.quit()

    def procesar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self._abierta = False
                pygame.quit()
                return False

        return self._abierta

    def esperar(self, segundos):
        inicio = pygame.time.get_ticks()

        while pygame.time.get_ticks() - inicio < segundos * 1000:
            if not self.procesar_eventos():
                return False

            pygame.time.delay(10)

        return True

    def leer_entrada(self, mensaje=""):
        if os.name != "nt":
            return input(mensaje)

        print(mensaje, end="", flush=True)
        caracteres = []

        while self._abierta:
            if not self.procesar_eventos():
                raise SystemExit

            if msvcrt.kbhit():
                caracter = msvcrt.getwch()

                if caracter == "\r":
                    print()
                    return "".join(caracteres)

                if caracter == "\b":
                    if caracteres:
                        caracteres.pop()
                        print("\b \b", end="", flush=True)
                    continue

                if caracter in ("\x00", "\xe0"):
                    msvcrt.getwch()
                    continue

                if caracter == "\x03":
                    raise KeyboardInterrupt

                if caracter.isprintable():
                    caracteres.append(caracter)
                    print(caracter, end="", flush=True)

            pygame.time.delay(10)

        raise SystemExit

    def esperar_enter(self, mensaje=""):
        self.leer_entrada(mensaje)

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

        if posicion == 0:
            etiqueta = self._fuente_casilla.render("INICIO", True, COLOR_TEXTO)
            self._pantalla.blit(etiqueta, (rect.centerx - etiqueta.get_width() // 2, rect.bottom - 20))
        elif posicion == CASILLA_FINAL:
            etiqueta = self._fuente_casilla.render("FIN", True, COLOR_TEXTO)
            self._pantalla.blit(etiqueta, (rect.centerx - etiqueta.get_width() // 2, rect.bottom - 20))

    def dibujar_fichas(self, posicion):
        fichas = self._tablero.casillas[posicion]

        if not fichas:
            return

        rect = rectangulo_casilla(posicion)
        radio = 13
        centro_x = rect.centerx
        centro_y = rect.centery + 6

        # Las fichas apiladas se dibujan en fila para que se vean todas.
        ancho_total = (len(fichas) - 1) * (radio + 2)
        inicio_x = centro_x - ancho_total // 2

        for i, ficha in enumerate(fichas):
            centro = (inicio_x + i * (radio + 2), centro_y)

            pygame.draw.circle(self._pantalla, COLORES_FICHA[ficha.color], centro, radio)
            pygame.draw.circle(self._pantalla, COLOR_BORDE, centro, radio, width=2)

            inicial = self._fuente_ficha.render(ficha.color.name[0], True, (255, 255, 255))
            self._pantalla.blit(
                inicial,
                (centro[0] - inicial.get_width() // 2, centro[1] - inicial.get_height() // 2),
            )

    def dibujar_panel(self):
        panel = pygame.Rect(
            MARGEN + TAM_CASILLA + 24,
            MARGEN + TAM_CASILLA + 24,
            (COLUMNAS - 2) * TAM_CASILLA - 48,
            (FILAS - 2) * TAM_CASILLA - 48,
        )

        pygame.draw.rect(self._pantalla, COLOR_PANEL, panel, border_radius=18)
        pygame.draw.rect(self._pantalla, COLOR_BORDE_PANEL, panel, width=2, border_radius=18)

        titulo = self._fuente_titulo.render("JUEGO DE TABLERO", True, COLOR_TEXTO_PANEL)
        self._pantalla.blit(titulo, (panel.centerx - titulo.get_width() // 2, panel.y + 32))

        if self._jugador_actual is not None:
            color = COLORES_FICHA[self._jugador_actual.color]
            turno = self._fuente_panel.render(
                f"Turno: {self._jugador_actual.nombre} ({self._jugador_actual.color.name})",
                True,
                color,
            )
            self._pantalla.blit(turno, (panel.centerx - turno.get_width() // 2, panel.y + 100))

        dado_texto = "-" if self._ultimo_dado is None else str(self._ultimo_dado)
        dado = self._fuente_dado.render(f"DADO: {dado_texto}", True, COLOR_TEXTO_PANEL)
        self._pantalla.blit(dado, (panel.centerx - dado.get_width() // 2, panel.y + 155))

        mensaje = self._fuente_panel.render(self._mensaje, True, COLOR_TEXTO_SECUNDARIO)
        self._pantalla.blit(mensaje, (panel.centerx - mensaje.get_width() // 2, panel.y + 245))

        leyenda_titulo = self._fuente_panel.render("CASILLAS ESPECIALES", True, COLOR_TEXTO_PANEL)
        self._pantalla.blit(
            leyenda_titulo,
            (panel.centerx - leyenda_titulo.get_width() // 2, panel.bottom - 130),
        )

        premio = self._fuente_casilla.render("P1 / P2 / P3  Premio", True, COLOR_CASILLA_ESPECIAL_POSITIVA)
        castigo = self._fuente_casilla.render("C1 / C2       Castigo", True, COLOR_CASILLA_ESPECIAL_NEGATIVA)
        self._pantalla.blit(premio, (panel.centerx - premio.get_width() // 2, panel.bottom - 88))
        self._pantalla.blit(castigo, (panel.centerx - castigo.get_width() // 2, panel.bottom - 58))

    def dibujar(self):
        if not self.procesar_eventos():
            return False

        self._pantalla.fill(COLOR_FONDO)

        for posicion in range(TOTAL_CASILLAS):
            self.dibujar_casilla(posicion)
            self.dibujar_fichas(posicion)

        self.dibujar_panel()

        pygame.display.flip()

        return True
