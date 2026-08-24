from Player import Player

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

        # TODO: Hacer calculo de la nueva posicion en base a si cayo en una casilla mala,
        # o si ya existia otra ficha en esa posicion.

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