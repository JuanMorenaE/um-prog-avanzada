class Promocion:
    def __init__(self, codigo):
        self.codigo = codigo
        self.nombre = None
        self.descuento = None
        self.condiciones = []

    def cuando_producto(self, producto):
        return self