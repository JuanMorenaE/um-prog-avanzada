class Supermercado:
    def __init__(self):
        self.productos = {}
        self.promociones = {}

    def agregar_producto(self, producto):
        if producto.codigo in self.productos:
            raise ValueError(f"Ya existe un producto con el codigo {producto.codigo}")

        producto.validar()
        self.productos[producto.codigo] = producto

    def agregar_promocion(self, promocion):
        if promocion.codigo in self.promociones:
            raise ValueError(f"Ya existe una promocion con el codigo {promocion.codigo}")

        promocion.validar()
        self.promociones[promocion.codigo] = promocion

    def obtener_producto(self, codigo):
        if codigo not in self.productos:
            raise ValueError(f"No existe un producto con el codigo {codigo}")

        return self.productos[codigo]
