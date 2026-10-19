from Clases.Producto import Producto

class DSLSupermercado:
    def __init__(self):
        self.actual = None
        self.productos = {}

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

    def finalizar(self):
        return self