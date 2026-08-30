from enum import Enum
import time

class Color(Enum):
    ROJO = 1
    VERDE = 2
    AZUL = 3
    AMARILLO = 4


def logDecorator(function):
    start = time.time()
    function()
    print(f"[LOG] {function.name} tardó {time.time() - start:.4f} segundos")