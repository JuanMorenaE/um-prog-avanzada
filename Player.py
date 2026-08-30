from Ficha import Ficha
from functools import reduce
from Constantes import CASILLA_FINAL

class Player:
    def __init__(self, name, color):
        self.max_fichas = 4
        self.nombre = name
        self.color = color
        self.fichas = []
        self.pierde_proximo_turno = False

    def es_ganador(self):
        return len(filter(lambda f: f.posicion == CASILLA_FINAL, self.fichas)) == self.max_fichas


    
