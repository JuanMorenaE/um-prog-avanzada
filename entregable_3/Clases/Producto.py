class Producto:
    def __init__(self, codigo):
        self.codigo = codigo
        self.nombre = None
        self.categoria = None
        self.precio = None

    def __str__(self):
        return f"{self.nombre} ${self.precio} - Categoria: {self.categoria}"