from Clases.Condicion import Operador
from Clases.Producto import Producto
from Clases.Promocion import Promocion
from Clases.Supermercado import Supermercado

class DSLSupermercado:
    def __init__(self):
        self.supermercado = Supermercado()
        self.actual = None
        self.condicion_actual = None

    def producto(self, codigo):
        self._cerrar_actual()
        self.actual = Producto(codigo)
        return self

    def nombre(self, nombre):
        if self.actual is None:
            raise ValueError("'nombre' debe usarse luego de 'producto' o 'promocion'")

        self.actual.nombre = nombre
        return self

    def precio(self, precio):
        self._producto_actual("precio").precio = precio
        return self

    def categoria(self, categoria):
        self._producto_actual("categoria").categoria = categoria
        return self

    def promocion(self, codigo):
        self._cerrar_actual()
        self.actual = Promocion(codigo)
        return self

    def descuento(self, descuento):
        self._promocion_actual("descuento").descuento = descuento
        return self

    def cuando_producto(self, codigo):
        promocion = self._promocion_actual("cuando_producto")
        producto = self.supermercado.obtener_producto(codigo)

        self.condicion_actual = promocion.agregar_condicion(producto)
        return self

    def cantidad_igual(self, cantidad):
        condicion = self._condicion_actual("cantidad_igual")
        condicion.operador = Operador.IGUAL
        condicion.cantidad = cantidad
        return self

    def cantidad_mayor_igual(self, cantidad):
        condicion = self._condicion_actual("cantidad_mayor_igual")
        condicion.operador = Operador.MAYOR_IGUAL
        condicion.cantidad = cantidad
        return self

    def finalizar(self):
        self._cerrar_actual()
        print("Se finalizo la carga del supermercado")
        return self.supermercado

    def _cerrar_actual(self):
        if isinstance(self.actual, Producto):
            self.supermercado.agregar_producto(self.actual)
        elif isinstance(self.actual, Promocion):
            self.supermercado.agregar_promocion(self.actual)

        self.actual = None
        self.condicion_actual = None

    def _producto_actual(self, metodo):
        if not isinstance(self.actual, Producto):
            raise ValueError(f"'{metodo}' debe usarse luego de 'producto'")

        return self.actual

    def _promocion_actual(self, metodo):
        if not isinstance(self.actual, Promocion):
            raise ValueError(f"'{metodo}' debe usarse luego de 'promocion'")

        return self.actual

    def _condicion_actual(self, metodo):
        if self.condicion_actual is None:
            raise ValueError(f"'{metodo}' debe usarse luego de 'cuando_producto'")

        return self.condicion_actual
