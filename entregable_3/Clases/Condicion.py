from enum import Enum

class Operador(Enum):
    IGUAL = "="
    MAYOR_IGUAL = ">="

class Condicion:
    def __init__(self, producto):
        self.producto = producto
        self.operador = Operador.IGUAL
        self.cantidad = 1

    def validar(self):
        if not isinstance(self.operador, Operador):
            raise ValueError(f"Operador invalido '{self.operador}' para el producto {self.producto.codigo}")
        if not isinstance(self.cantidad, int) or self.cantidad < 1:
            raise ValueError(f"La cantidad del producto {self.producto.codigo} debe ser un entero mayor o igual a 1 (recibido: {self.cantidad})")

    def __str__(self):
        return f"Producto {self.producto.codigo} {self.producto.nombre}: cantidad {self.operador.value} {self.cantidad}"
