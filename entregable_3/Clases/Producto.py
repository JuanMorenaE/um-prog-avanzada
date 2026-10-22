class Producto:
    def __init__(self, codigo):
        self.codigo = codigo
        self.nombre = None
        self.categoria = None
        self.precio = None

    def validar(self):
        if not isinstance(self.codigo, int):
            raise ValueError(f"El codigo de producto debe ser un entero (recibido: {self.codigo})")
        if not isinstance(self.nombre, str):
            raise ValueError(f"El producto {self.codigo} debe tener un nombre de tipo texto")
        if self.categoria is not None and not isinstance(self.categoria, str):
            raise ValueError(f"La categoria del producto {self.codigo} debe ser de tipo texto")
        if not isinstance(self.precio, (int, float)) or self.precio <= 0 or round(self.precio, 2) != self.precio:
            raise ValueError(f"El producto {self.codigo} debe tener un precio mayor a 0 con hasta 2 decimales (recibido: {self.precio})")

    def __str__(self):
        categoria = self.categoria or "Sin categoria"
        return f"{self.codigo}. {self.nombre} - ${self.precio:.2f} ({categoria})"
