
class Compra:
    def __init__(self):
        self.productos = []
        self.promociones = []
        self.importe = 0

    def agregar_producto(self, producto, cantidad):
        linea = {
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": cantidad,
            "descuento": 0,
            "subtotal": producto.precio * cantidad,
            "promociones": [],
        }

        self.productos.append(linea)
        self.importe += linea["subtotal"]

    def aplicar_promociones(self, promociones):
        # Agrupar cantidades por código de producto
        disponibles = {}
        datos_productos = {}

        for linea in self.productos:
            codigo = linea["codigo"]
            disponibles[codigo] = (
                disponibles.get(codigo, 0) + linea["cantidad"]
            )
            datos_productos[codigo] = linea

        nuevas_lineas = []
        self.promociones = []

        # Priorizar promociones de mayor descuento
        promociones_ordenadas = sorted(
            promociones,
            key=lambda p: (-p.descuento, p.codigo)
        )

        for promocion in promociones_ordenadas:
            cantidades = {
                condicion.producto.codigo: condicion.cantidad
                for condicion in promocion.condiciones
            }

            # Repetir mientras haya unidades suficientes
            while all(
                disponibles.get(codigo, 0) >= cantidad
                for codigo, cantidad in cantidades.items()
            ):
                for codigo, cantidad in cantidades.items():
                    disponibles[codigo] -= cantidad

                    producto = datos_productos[codigo]
                    subtotal = (
                        producto["precio"]
                        * cantidad
                        * (1 - promocion.descuento / 100)
                    )

                    nuevas_lineas.append({
                        "codigo": codigo,
                        "nombre": producto["nombre"],
                        "precio": producto["precio"],
                        "cantidad": cantidad,
                        "descuento": promocion.descuento,
                        "subtotal": round(subtotal, 2),
                        "promociones": [promocion.codigo],
                    })

                if promocion.codigo not in self.promociones:
                    self.promociones.append(promocion.codigo)

        # Agregar unidades que no recibieron descuentos
        for codigo, cantidad in disponibles.items():
            if cantidad > 0:
                producto = datos_productos[codigo]

                nuevas_lineas.append({
                    "codigo": codigo,
                    "nombre": producto["nombre"],
                    "precio": producto["precio"],
                    "cantidad": cantidad,
                    "descuento": 0,
                    "subtotal": producto["precio"] * cantidad,
                    "promociones": [],
                })

        self.productos = nuevas_lineas
        self.importe = round(
            sum(linea["subtotal"] for linea in self.productos),
            2
        )

    def __str__(self):
        resultado = "COMPRA\n"

        for linea in self.productos:
            resultado += (
                f"  {linea['nombre']} x{linea['cantidad']} "
                f"- ${linea['subtotal']:.2f}"
            )

            if linea["descuento"] > 0:
                resultado += (
                    f" ({linea['descuento']}% OFF, "
                    f"promoción {linea['promociones'][0]})"
                )

            resultado += "\n"

        resultado += f"TOTAL: ${self.importe:.2f}"
        return resultado
