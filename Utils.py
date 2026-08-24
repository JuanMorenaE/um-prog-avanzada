import random
import math
from enum import Enum

def tirar_dados():
    return math.floor(random.random() * 6) + 1

class Color(Enum):
    ROJO = 1
    VERDE = 2
    AZUL = 3
    AMARILLO = 4