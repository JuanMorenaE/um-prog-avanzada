from Player import Player
from Dados import Dados
from Utils import Color
from Ficha import Ficha
from Constantes import TOTAL_CASILLAS, CASILLA_FINAL
from Opciones import mostrar_opciones

class Tablero:    
    def __init__(self):
        self.casillas = [[] for _ in range (TOTAL_CASILLAS)]
        self.auto_mode = False


    # -----------------------------
    #          FICHAS
    # -----------------------------

    def sacar_ficha(self, jugador: Player):
        if len(jugador.fichas) >= jugador.max_fichas:
            return

        ficha = Ficha(jugador.color, 0)
        jugador.fichas.append(ficha)

        self.casillas[0].append(ficha)


    def calcular_posicion(self, posicion: int, dado: int):
        return min(posicion + dado, CASILLA_FINAL)


    def mover_ficha(self, ficha: Ficha, dados: int, jugadores: list[Player]):
        pos_actual = ficha.posicion
        pos_nueva =  self.calcular_posicion(pos_actual, dados)

        if pos_nueva == CASILLA_FINAL:
            print("¡Una ficha llegó al final!")

        fichas_en_casilla = self.casillas[pos_nueva]

        # No hay fichas en la nueva posicion o hay pero son del mismo color o es la casilla final.
        if len(fichas_en_casilla) == 0 or fichas_en_casilla[0].color == ficha.color or pos_nueva == CASILLA_FINAL:
            self.avanzar_ficha(ficha, pos_actual, pos_nueva)
            return


        self.competencia_por_posicion(ficha, pos_actual, pos_nueva, jugadores)


    def avanzar_ficha(self, ficha: Ficha, pos_actual: int, pos_nueva: int):
        self.casillas[pos_actual].remove(ficha)
        self.casillas[pos_nueva].append(ficha)
        ficha.posicion = pos_nueva


    def retroceder_ficha(self, ficha: Ficha, pos_actual: int, pos_nueva: int):
        # Si llegó a la primer casilla, no importa si hay jugadores queda ahí.
        if pos_nueva <= 0:
            pos_nueva = 0
            self.casillas[pos_actual].remove(ficha)
            self.casillas[pos_nueva].append(ficha)
            ficha.posicion = 0
            return
        
        fichas_en_casilla = self.casillas[pos_nueva]

        # No hay fichas en la nueva posicion o hay pero son del mismo color.
        if len(fichas_en_casilla) == 0 or fichas_en_casilla[0].color == ficha.color:
            self.casillas[pos_actual].remove(ficha)
            self.casillas[pos_nueva].append(ficha)
            ficha.posicion = pos_nueva
            return

        self.retroceder_ficha(ficha, pos_actual, pos_nueva - 1)


    def competencia_por_posicion(self, ficha: Ficha, pos_actual: int, pos_nueva: int, players: list[Player]):
        ficha_rival = self.casillas[pos_nueva][0]

        player_actual = next(filter(lambda p: p.color == ficha.color, players))
        player_rival = next(filter(lambda p: p.color == ficha_rival.color, players))

        ganador = self.competencia_dados(player_actual, player_rival)

        if ganador == 1:
            # Ganó el que se movió.
            self.casillas[pos_actual].remove(ficha)
            self.casillas[pos_nueva].append(ficha)
            ficha.posicion = pos_nueva

            self.retroceder_ficha(ficha_rival, pos_nueva, pos_nueva - 2)
        else:
            # Ganó el que ya estaba en la casilla.
            self.retroceder_ficha(ficha, pos_actual, pos_nueva - 2)


    def competencia_dados(self, player1: Player, player2: Player):
        print("\n╔════════════════════════════════════╗")
        print(f"\t⚔ COMPETENCIA ⚔")
        print(f"\t{player1.nombre} vs {player2.nombre}")
        print("╚════════════════════════════════════╝")
        
        while True:
            if not self.auto_mode:
                input(f"\nTurno de {player1.nombre}, presioná ENTER para tirar los dados...")

            player1_score = Dados.tirar_dados()
            print(f"\n\t⚁ DADO: {player1_score} ⚁")

            if not self.auto_mode:
                input(f"\nTurno de {player2.nombre}, presioná ENTER para tirar los dados....")

            player2_score = Dados.tirar_dados()
            print(f"\n\t⚁ DADO: {player2_score} ⚁")

            if player1_score > player2_score:
                if not self.auto_mode:
                    input(f"\n{player1.nombre} gana la competencia. \n{player2.nombre} retrocede 2 casillas.")
                return 1
            elif player2_score > player1_score:
                if not self.auto_mode:
                    input(f"\n{player2.nombre} gana la competencia. \n{player1.nombre} retrocede 2 casillas.")
                return 2
            else:
                if not self.auto_mode:
                    input("\nEmpate, se vuelve a tirar...")