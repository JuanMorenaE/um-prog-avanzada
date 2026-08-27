from Ficha import Ficha

class Player:
    def __init__(self, name, color):
        self._max_fichas = 4
        self._name = name
        self._color = color
        self._fichas = [] # Un jugador puede tener mas de 1 ficha para mover.

        ##Bien básico, podriamos meterle debuffs segun la casilla en la que cae o alguna cosa medio falopa. Despues vemos

    def avanzar(self, cantidad):
        self._posicion += cantidad

    def sacar_ficha(self):
        if len(self._fichas) >= self._max_fichas:
            return

        ficha = Ficha(self._color, 0)
        self._fichas.append(ficha)

        return ficha

    def ganador(self, casilla_final):
        fichas_finalizadas = 0

        for ficha in self._fichas:
            if ficha._posicion == casilla_final:
                fichas_finalizadas += 1

        if fichas_finalizadas == self._max_fichas:
            return True

        return False


    
