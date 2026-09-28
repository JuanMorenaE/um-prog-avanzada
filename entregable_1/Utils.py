from enum import Enum
import time

class Color(Enum):
    ROJO = 1
    VERDE = 2
    AZUL = 3
    AMARILLO = 4


def componer(f, g):
    return lambda x: f(g(x))


nombre_color = componer(
    str.capitalize,
    lambda color: color.name
)


def logDecorator(function):
    def wrapper():
        start = time.time()
        result = function()
        print(f"[LOG] {function.__name__} tardó {time.time() - start:.4f} segundos")

        return result

    return wrapper
