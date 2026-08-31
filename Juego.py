from Tablero import Tablero, CASILLA_FINAL
from Player import Player
from Dados import Dados
from Opciones import mostrar_opciones
from Constantes import MAX_JUGADORES
from Vista import Vista
from Ficha import Ficha
from Utils import Color


class Juego:
    def __init__(self):
        self.auto_mode = False

        self.jugadores = []
        self.max_jugadores = MAX_JUGADORES

        self.tablero = Tablero()
        self.vista = Vista(self)
        self.tablero.esperar_enter = self.vista.esperar_enter

        self.casillas_especiales = {
            5: self.efecto_P1,
            11: self.efecto_P2,
            16: self.efecto_C1,
            22: self.efecto_P3,
            29: self.efecto_C2,
        }


    # -----------------------------
    #          JUGADORES
    # -----------------------------

    def nuevo_jugador(self, name: str, color: Color):
        if len(self.jugadores) >= self.max_jugadores:
            print("\n[ ERROR ] No se pueden añadir mas jugadores.")
            return
        
        jugador = Player(name, color)

        self.jugadores.append(jugador)
        self.tablero.sacar_ficha(jugador)     

        return jugador


    def obtener_jugador_por_color(self, color: Color):
        return next(filter(lambda x: x.color == color, self.jugadores), None)


    # -----------------------------
    #          TURNO
    # -----------------------------

    def turno_jugador(self, jugador: Player):
        if jugador.pierde_proximo_turno:
            print("\nEl jugador pierde el turno...")
            if not self.auto_mode:
                self.vista.esperar_enter()

            jugador.pierde_proximo_turno = False
            return

        if not self.auto_mode:
            self.vista.esperar_enter("\nPresioná ENTER para tirar los dados...")

        dados = Dados.tirar_dados()

        print(f"\n\t⚁ DADO: {dados} ⚁")

        print("\n¿Qué querés hacer?")

        opciones = {}

        if len(jugador.fichas) != jugador.max_fichas:
            opciones[f"Sacar una ficha ({len(jugador.fichas)}/{jugador.max_fichas})"] = lambda: self.sacar_ficha(jugador)

        if len(jugador.fichas) != 0:
            opciones[f"Mover una ficha"] = lambda: self.mover_ficha(jugador, dados)

        funcion = mostrar_opciones(opciones, self.auto_mode, self.vista.leer_entrada)
        funcion()

 
    def sacar_ficha(self, jugador: Player):
        self.tablero.sacar_ficha(jugador)
        self.vista.dibujar()


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

                selected_ficha = mostrar_opciones(opciones, self.auto_mode, self.vista.leer_entrada)

                if selected_ficha in fichas_validas:
                    break

                print(f"Opción inválida, selecciona una opción disponible ({fichas_validas})")
            except ValueError:
                print(f"Opción inválida, selecciona una opción disponible ({fichas_validas})")

        ficha = jugador.fichas[selected_ficha - 1]
        self.tablero.mover_ficha(ficha, dados, self.jugadores)

        print(f"\n✓ Ficha movida a la posicion {ficha.posicion}.")

        self.vista.dibujar()

        self.aplicar_casilla_especial(ficha, jugador)

        self.vista.dibujar()


    # -----------------------------
    #      CASILLAS ESPECIALES
    # -----------------------------

    def obtener_casilla_especial(self, posicion: int):
        return self.casillas_especiales.get(posicion)

    
    def aplicar_casilla_especial(self, ficha: Ficha, player: Player):
        efecto = self.obtener_casilla_especial(ficha.posicion)
        
        if efecto is None:
            return None

        efecto(ficha, player)


    def efecto_P1(self, ficha: Ficha, player: Player): # Elige un color para que pierda un turno
        if not self.auto_mode:
            self.vista.esperar_enter("\nCaíste en la casilla P1: 'Elige un color para que pierda un turno'.")

        candidatos = (p for p in self.jugadores if p != player)

        while True:
            print()
            opciones = {}
            for candidato in candidatos:
                opciones[f"{candidato.color.name} - {candidato.nombre}"] = candidato.color

            color = mostrar_opciones(opciones, self.auto_mode, self.vista.leer_entrada)

            player_pierde_turno = next(filter(lambda p: p.color == color, self.jugadores))
            player_pierde_turno.pierde_proximo_turno = True

            if not self.auto_mode:
                self.vista.esperar_enter(f"\nEl jugador '{player_pierde_turno.nombre}' pierde un turno.")

            return
        

    def efecto_P2(self, ficha: Ficha, player: Player): # Tira el dado nuevamente y avanza
        if not self.auto_mode:
            self.vista.esperar_enter("\nCaíste en la casilla P2: 'Tira el dado nuevamente y avanza'.")
            self.vista.esperar_enter("\nPresioná ENTER para tirar los dados...")

        dados = Dados.tirar_dados()
        print(f"\n\t⚁ DADO: {dados} ⚁")

        self.tablero.mover_ficha(ficha, dados, self.jugadores)
        if not self.auto_mode:
            self.vista.esperar_enter(f"\n✓ Ficha movida {dados} posiciones.")


    def efecto_P3(self, ficha: Ficha, player: Player): # Avanza 2 casillas
        if not self.auto_mode:
            self.vista.esperar_enter("\nCaíste en la casilla P3: ' Avanza 2 casillas'.")

        self.tablero.mover_ficha(ficha, 2, self.jugadores)

        if not self.auto_mode:
            self.vista.esperar_enter("\n✓ Ficha movida 2 posiciones.")


    def efecto_C1(self, ficha: Ficha, player: Player): #  Pierde 1 turno
        if not self.auto_mode:
            self.vista.esperar_enter("\nCaíste en la casilla C1: 'Pierde 1 turno'.")
        player.pierde_proximo_turno = True


    def efecto_C2(self, ficha: Ficha, player: Player): # Retrocede 3 casillas
        if not self.auto_mode:
            self.vista.esperar_enter("\nCaíste en la casilla C2: 'Retrocede 3 casillas'.")

        self.tablero.mover_ficha(ficha, -3, self.jugadores)

        if not self.auto_mode:
            self.vista.esperar_enter("\n✓ Ficha retrocede 3 posiciones.")
