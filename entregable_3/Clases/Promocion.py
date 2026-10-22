from Clases.Condicion import Condicion

class Promocion:
    def __init__(self, codigo):
        self.codigo = codigo
        self.nombre = None
        self.descuento = None
        self.condiciones = []

    def agregar_condicion(self, producto):
        if any(condicion.producto.codigo == producto.codigo for condicion in self.condiciones):
            raise ValueError(f"La promocion {self.codigo} ya tiene una condicion para el producto {producto.codigo}")

        condicion = Condicion(producto)
        self.condiciones.append(condicion)
        return condicion

    def validar(self):
        if not isinstance(self.codigo, int):
            raise ValueError(f"El codigo de promocion debe ser un entero (recibido: {self.codigo})")
        if not isinstance(self.nombre, str):
            raise ValueError(f"La promocion {self.codigo} debe tener un nombre de tipo texto")
        if not isinstance(self.descuento, (int, float)) or not 0 < self.descuento <= 100:
            raise ValueError(f"La promocion {self.codigo} debe tener un descuento entre 0 y 100 (recibido: {self.descuento})")
        if not self.condiciones:
            raise ValueError(f"La promocion {self.codigo} debe tener al menos una condicion")

        for condicion in self.condiciones:
            condicion.validar()

    def __str__(self):
        text = f"{self.codigo}. {self.nombre} - {self.descuento}% OFF"

        for condicion in self.condiciones:
            text += f"\n\t- {condicion}"

        return text
