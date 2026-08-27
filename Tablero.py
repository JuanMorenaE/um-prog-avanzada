from Player import Player
from Dados import Dados

TOTAL_CASILLAS = 36
CASILLA_FINAL = TOTAL_CASILLAS - 1
MAX_JUGADORES = 4

class Tablero:
    def __init__(self):
        self._casillas = [[] for _ in range (TOTAL_CASILLAS)]
        self._max_players = MAX_JUGADORES
        self._players = []

    # -----------------------------
    #          JUGADORES
    # -----------------------------

    def nuevo_jugador(self, name, color):
        if len(self._players) >= self._max_players:
            print("\n[ ERROR ] No se pueden añadir mas jugadores.")
            return
        
        player = Player(name, color)
        self._players.append(player)

        return player


    def buscar_jugador_por_color(self, color):
        return next(filter(lambda x: x._color == color, self._players))


    # -----------------------------
    #          FICHAS
    # -----------------------------

    def calcular_posicion(self, posicion, dado):
        return min(posicion + dado, CASILLA_FINAL)


    def mover_ficha(self, ficha, dados):
        pos_actual = ficha._posicion
        pos_nueva =  self.calcular_posicion(pos_actual, dados)

        if pos_nueva == CASILLA_FINAL:
            print("¡Una ficha llegó al final!")

        fichas_en_casilla = self._casillas[pos_nueva]

        # No hay fichas en la nueva posicion o hay pero son del mismo color.
        if len(fichas_en_casilla) == 0 or fichas_en_casilla[0]._color == ficha._color:
            self.avanzar_ficha(ficha, pos_actual, pos_nueva)
            return


        self.competencia_por_posicion(ficha, pos_actual, pos_nueva)


    def avanzar_ficha(self, ficha, pos_actual, pos_nueva):
        self._casillas[pos_actual].remove(ficha)
        self._casillas[pos_nueva].append(ficha)
        ficha._posicion = pos_nueva

    def retroceder_ficha(self, ficha, pos_actual, pos_nueva):
        # Si llegó a la primer casilla, no importa si hay jugadores queda ahí.
        if pos_nueva <= 0:
            pos_nueva = 0
            self._casillas[pos_actual].remove(ficha)
            self._casillas[pos_nueva].append(ficha)
            ficha._posicion = 0
            return
        
        fichas_en_casilla = self._casillas[pos_nueva]

        # No hay fichas en la nueva posicion o hay pero son del mismo color.
        if len(fichas_en_casilla) == 0 or fichas_en_casilla[0]._color == ficha._color:
            self._casillas[pos_actual].remove(ficha)
            self._casillas[pos_nueva].append(ficha)
            ficha._posicion = pos_nueva
            return

        self.retroceder_ficha(ficha, pos_actual, pos_nueva - 1)
    

    def mostrar_tablero(self):
        # Esta funcion me la hizo el chat para ver momentaneamente.
        print("\nTABLERO")
        print("─" * 50)

        for i, casilla in enumerate(self._casillas):

            if len(casilla) == 0:
                contenido = "·"
            else:
                contenido = ",".join(
                    ficha._color.name[0]
                    for ficha in casilla
                )

            print(f"[{i:02}] {contenido}", end="  ")

            if (i + 1) % 6 == 0:
                print()

        print("─" * 50)


    def competencia_por_posicion(self, ficha, pos_actual, pos_nueva):
        ficha_rival = self._casillas[pos_nueva][0]

        player_actual = self.buscar_jugador_por_color(ficha._color)
        player_rival = self.buscar_jugador_por_color(ficha_rival._color)

        ganador = self.competencia_dados(player_actual, player_rival)

        if ganador == 1:
            # Ganó el que se movió.
            self._casillas[pos_actual].remove(ficha)
            self._casillas[pos_nueva].append(ficha)
            ficha._posicion = pos_nueva

            self.retroceder_ficha(ficha_rival, pos_nueva, pos_nueva - 2)
        else:
            # Ganó el que ya estaba en la casilla.
            self.retroceder_ficha(ficha, pos_actual, pos_nueva - 2)


    def competencia_dados(self, player1, player2):
        while True:
            input(f"Turno de {player1._name}, presione ENTER para tirar los dados.")
            player1_score = Dados.tirar_dados()
            print("\n────────────────────────────────────")
            print(f"DADO: [{player1_score}]")
            print("────────────────────────────────────")

            input(f"Turno de {player2._name}, presione ENTER para tirar los dados.")
            player2_score = Dados.tirar_dados()
            print("\n────────────────────────────────────")
            print(f"DADO: [{player2_score}]")
            print("────────────────────────────────────")

            if player1_score > player2_score:
                print(f"El ganador es {player1._name}.")
                return 1
            elif player2_score > player1_score:
                print(f"El ganador es {player2._name}.")
                return 2
