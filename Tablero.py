from Player import Player
from Dados import Dados

class Tablero:
    def __init__(self):
        self._casillas = [[] for _ in range (36)]
        self._max_players = 4
        self._players = []

    def new_player(self, name, color):
        if len(self._players) >= self._max_players:
            print("\n[ ERROR ] No se pueden añadir mas jugadores.")
            return
        
        player = Player(name, color)
        self._players.append(player)

    def mover_ficha(self, ficha, dados):
        pos_actual = ficha._posicion
        pos_nueva = ficha._posicion + dados

        if pos_nueva > 35:
            pos_nueva = 35

        if pos_nueva == 35:
            print("Una ficha llego al final!")

        # Verificamos si hay otras fichas.
        if len(self._casillas[pos_nueva]) != 0:

            # Si son del mismo color, no pasa nada
            if self._casillas[pos_nueva][0]._color != ficha._color:

                print("Se tiran dados para ver quien gana!!!!!")
                player1 = list(filter(lambda x: x._color == ficha._color, self._players))[0]
                player2 = list(filter(lambda x: x._color == self._casillas[pos_nueva][0]._color, self._players))[0]

                print(f"La competencia es entre {player1._name} y {player2._name}!!!")
                if self.compete_for_position(player1, player2) == 1:
                    ficha_contraria = self._casillas[pos_nueva][0]
                    self._casillas[pos_nueva].remove(ficha_contraria)

                    self._casillas[pos_nueva - 2].append(ficha_contraria)
                    self._casillas[pos_nueva].append(ficha)

                    ficha_contraria._posicion = pos_nueva - 2
                    ficha._posicion = pos_nueva
                else:
                    self._casillas[pos_nueva - 2].append(ficha)
                    ficha._posicion = pos_nueva - 2
        else:
            ficha._posicion = pos_nueva

            self._casillas[pos_actual].remove(ficha)
            self._casillas[pos_nueva].append(ficha)


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

    def compete_for_position(self, player1, player2):
        winner = None

        while winner == None:
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
                winner = 1
                print(f"El ganador es {player1._name}. {player2._name} retrocede 2 casillas.")
            elif player2_score > player1_score:
                winner = 2
                print(f"El ganador es {player2._name}. {player1._name} retrocede 2 casillas.")