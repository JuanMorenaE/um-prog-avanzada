class Supermercado:
    def __init__(self):
        self.productos = {}
        self.promociones = {}
        self.compras = []

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

    def obtener_promocion(self, codigo):
        if codigo not in self.promociones:
            raise ValueError(f"No existe una promoción con el codigo {codigo}")

        return self.promociones[codigo]

    def eliminar_producto(self, codigo):
        if codigo not in self.productos:
            raise ValueError(f"No existe un producto con el codigo {codigo}")

        promociones = [
            promocion.codigo
            for promocion in self.promociones.values()
            if any(condicion.producto.codigo == codigo for condicion in promocion.condiciones)
        ]
        if promociones:
            raise ValueError(f"El producto {codigo} esta en las promociones {promociones}, eliminelas primero")

        del self.productos[codigo]

    def eliminar_promocion(self, codigo):
        if codigo not in self.promociones:
            raise ValueError(f"No existe una promoción con el codigo {codigo}")

        del self.promociones[codigo]

    def registrar_compra(self, compra):
        self.compras.append(compra)