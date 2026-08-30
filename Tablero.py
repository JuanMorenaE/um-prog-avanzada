from Player import Player
from Dados import Dados
from Utils import Color
from Ficha import Ficha
from Constantes import TOTAL_CASILLAS, CASILLA_FINAL

class Tablero:    
    def __init__(self):
        self.casillas = [[] for _ in range (TOTAL_CASILLAS)]
        self.casillas_especiales = {
            5: self.efecto_P1,
            11: self.efecto_P2,
            16: self.efecto_C1,
            22: self.efecto_P3,
            29: self.efecto_C2,
        }


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


    def mover_ficha(self, ficha: Ficha, dados: int):
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


    def avanzar_ficha(self, ficha: Ficha, pos_actual: int, pos_nueva: int):
        self._casillas[pos_actual].remove(ficha)
        self._casillas[pos_nueva].append(ficha)
        ficha._posicion = pos_nueva


    def retroceder_ficha(self, ficha: Ficha, pos_actual: int, pos_nueva: int):
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


    def competencia_por_posicion(self, ficha: Ficha, pos_actual: int, pos_nueva: int):
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


    def competencia_dados(self, player1: Player, player2: Player):
        print("\n╔════════════════════════════════════╗")
        print(f"\t⚔ COMPETENCIA ⚔")
        print(f"\t{player1._name} vs {player2._name}")
        print("╚════════════════════════════════════╝")
        
        while True:
            input(f"\nTurno de {player1._name}, presioná ENTER para tirar los dados...")
            player1_score = Dados.tirar_dados()
            print(f"\n\t⚁ DADO: {player1_score} ⚁")

            input(f"\nTurno de {player2._name}, presioná ENTER para tirar los dados....")
            player2_score = Dados.tirar_dados()
            print(f"\n\t⚁ DADO: {player2_score} ⚁")

            if player1_score > player2_score:
                input(f"\n{player1._name} gana la competencia. \n{player2._name} retrocede 2 casillas.")
                return 1
            elif player2_score > player1_score:
                input(f"\n{player2._name} gana la competencia. \n{player1._name} retrocede 2 casillas.")
                return 2
            else:
                input("\nEmpate, se vuelve a tirar...")


    # -----------------------------
    #      CASILLAS ESPECIALES
    # -----------------------------

    def obtener_casilla_especial(self, posicion: int):
        return self._casillas_especiales.get(posicion)

    
    def aplicar_casilla_especial(self, ficha: Ficha, player: Player):
        efecto = self.obtener_casilla_especial(ficha._posicion)
        
        if efecto is None:
            return None

        efecto(ficha, player)
    

    def efecto_P1(self, ficha: Ficha, player: Player): # Elige un color para que pierda un turno
        input("\nCaíste en la casilla P1: 'Elige un color para que pierda un turno'.")

        candidatos = [p for p in self._players if p != player]

        while True:
            print()
            for candidato in candidatos:
                print(f"\t• {candidato._color.name}")

            color = input("\nElegí el color que va a perder un turno > ").upper()

            try:
                color = Color[color]
            except:
                input(f"\nx '{color}' no es un color válido. Presioná ENTER para continuar...")
                continue

            player_pierde_turno = next((p for p in candidatos if p._color == color), None)

            if player_pierde_turno is None:
                input(f"\nx '{color.name}' no es un color válido. Presioná ENTER para continuar...")
                continue

            player_pierde_turno._pierde_proximo_turno = True

            input(f"\nEl jugador '{player_pierde_turno._name}' pierde un turno.")

            return
        

    def efecto_P2(self, ficha: Ficha, player: Player): # Tira el dado nuevamente y avanza
        input("\nCaíste en la casilla P2: 'Tira el dado nuevamente y avanza'.")

        input("\nPresioná ENTER para tirar los dados...")
        
        dados = Dados.tirar_dados()

        print(f"\n\t⚁ DADO: {dados} ⚁")

        self.mover_ficha(ficha, dados)

        input(f"\n✓ Ficha movida {dados} posiciones.")
        
        pass


    def efecto_P3(self, ficha: Ficha, player: Player): # Avanza 2 casillas
        input("\nCaíste en la casilla P3: ' Avanza 2 casillas'.")

        self.mover_ficha(ficha, 2)
        
        input(f"\n✓ Ficha movida 2 posiciones.")

        pass


    def efecto_C1(self, ficha: Ficha, player: Player): #  Pierde 1 turno
        input("\nCaíste en la casilla C1: 'Pierde 1 turno'.")
        player._pierde_proximo_turno = True

        pass


    def efecto_C2(self, ficha: Ficha, player: Player): # Retrocede 3 casillas
        input("\nCaíste en la casilla C2: 'Retrocede 3 casillas'.")

        self.mover_ficha(ficha, -3)
                
        input(f"\n✓ Ficha retrocede 3 posiciones.")

        pass