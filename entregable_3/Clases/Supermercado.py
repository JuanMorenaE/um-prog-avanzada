from Clases.Producto import Producto
from Clases.Promocion import Promocion

class DSLSupermercado:
    def __init__(self):
        self.actual = None
        self.ultimoProducto = None
        self.productos = {}
        self.promociones = {}

    def producto(self, codigo):
        if codigo not in self.productos:
            self.productos[codigo] = Producto(codigo)

        self.actual = self.productos[codigo]
        return self

    def nombre(self, nombre):
        self.actual.nombre = nombre
        return self

    def precio(self, precio):
        self.actual.precio = precio
        return self

    def categoria(self, categoria):
        self.actual.categoria = categoria
        return self

    def promocion(self, codigo):
        if codigo not in self.promociones:
            self.promociones[codigo] = Promocion(codigo)
        
        self.actual = self.promociones[codigo]
        return self

    def descuento(self, descuento):
        self.actual.descuento = descuento
        return self

    def cuando_producto(self, codigo):
        if codigo not in self.productos:
            raise ValueError()

        self.ultimoProducto = codigo
        self.actual.condiciones[codigo] = { "operator": "equal", "quantity": 1 }
        return self

    def cantidad_igual(self, cantidad):
        self.actual.condiciones[self.ultimoProducto] = { "operator": "equal", "quantity": cantidad }
        return self

    def cantidad_mayor_igual(self, cantidad):
        self.actual.condiciones[self.ultimoProducto] = { "operator": "min", "quantity": cantidad }
        return self


    def finalizar(self):
        print("Se finalizo la carga del supermercado")
        return self