from Tablero import Tablero, CASILLA_FINAL
from Player import Player
from Dados import Dados
from Opciones import mostrar_opciones
from Constantes import MAX_JUGADORES
from Vista import Vista

class Juego:
    def __init__(self):
        self.auto_mode = False
        self.tablero = Tablero()
        self.jugadores = []
        self.max_jugadores = MAX_JUGADORES
        self.vista = Vista(self.tablero)


    # -----------------------------
    #          JUGADORES
    # -----------------------------

    def nuevo_jugador(self, name, color):
        if len(self.jugadores) >= self.max_jugadores:
            print("\n[ ERROR ] No se pueden añadir mas jugadores.")
            return
        
        jugador = Player(name, color)
        self.jugadores.append(jugador)
        self.tablero.sacar_ficha(jugador)     

        return jugador


    def obtener_jugador_por_color(self, color):
        return next(filter(lambda x: x.color == color, self.jugadores), None)


    # -----------------------------
    #          TURNO
    # -----------------------------

    def turno_jugador(self, jugador: Player):
        if jugador.pierde_proximo_turno:
            print("\nEl jugador pierde el turno...")
            if not self.auto_mode:
                input()

            jugador.pierde_proximo_turno = False
            return

        if not self.auto_mode:
            input("\nPresioná ENTER para tirar los dados...")

        dados = Dados.tirar_dados()

        print(f"\n\t⚁ DADO: {dados} ⚁")

        print("\n¿Qué querés hacer?")

        opciones = {}

        if len(jugador.fichas) != jugador.max_fichas:
            opciones[f"Sacar una ficha ({len(jugador.fichas)}/{jugador.max_fichas})"] = lambda: self.sacar_ficha(jugador)

        if len(jugador.fichas) != 0:
            opciones[f"Mover una ficha"] = lambda: self.mover_ficha(jugador, dados)

        funcion = mostrar_opciones(opciones, self.auto_mode)
        funcion()

 
    def sacar_ficha(self, jugador: Player):
        self.tablero.sacar_ficha(jugador)


    def mover_ficha(self, jugador: Player, dados: int):
        print("\n╔══════════════════════════╗")
        print("\tTUS FICHAS")
        print("╚══════════════════════════╝")

        fichas_validas = []
        opciones = {}

        while True:
            try:
                for index, ficha in enumerate(jugador.fichas, start=1):
                    if ficha.posicion != CASILLA_FINAL:
                        opciones[f"Posición: {ficha.posicion}"] = index
                        fichas_validas.append(index)
                    else:
                        opciones[f"Posición: {ficha.posicion} (¡Llegó a la meta!)"] = index

                selected_ficha = mostrar_opciones(opciones, self.auto_mode)

                if selected_ficha in fichas_validas:
                    break

                print(f"Opción inválida, selecciona una opción disponible ({fichas_validas})")
            except ValueError:
                print(f"Opción inválida, selecciona una opción disponible ({fichas_validas})")

        ficha = jugador.fichas[selected_ficha - 1]
        self.tablero.mover_ficha(ficha, dados)

        print(f"\n✓ Ficha movida a la posicion {ficha.posicion}.")
        self.vista.dibujar()
        self.tablero.aplicar_casilla_especial(ficha, jugador)
        self.vista.dibujar()