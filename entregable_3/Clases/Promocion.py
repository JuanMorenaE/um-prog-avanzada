class Promocion:
    def __init__(self, codigo):
        self.codigo = codigo
        self.nombre = None
        self.descuento = None
        self.condiciones = {}

    def __str__(self):
        text = f"{self.codigo} - {self.nombre} ({self.descuento}% OFF):"

        for codigo in self.condiciones:
            if (self.condiciones[codigo]["operator"] == "equal"):
                text += f"\n\tProducto {codigo}. Cantidad = {self.condiciones[codigo]["quantity"]}"
            else:
                text += f"\n\tProducto {codigo}. Cantidad > {self.condiciones[codigo]["quantity"]}"

        return text 