
from .parser import interpretar_compras_con_errores
from Clases.Compra import Compra



def ejecutar_compras(texto, supermercado):
    # El parser devuelve las compras y los errores sintácticos
    instrucciones, errores = interpretar_compras_con_errores(texto)

    compras_realizadas = []

    for numero, productos in enumerate(instrucciones, start=1):
        compra = Compra()

        for codigo, cantidad in productos:
            if cantidad <= 0:
                errores.append(
                    f"Compra {numero}: cantidad inválida "
                    f"para el producto {codigo}"
                )
                continue

            try:
                producto = supermercado.obtener_producto(codigo)
            except ValueError as error:
                errores.append(f"Compra {numero}: {error}")
                continue

            compra.agregar_producto(producto, cantidad)

        if compra.productos:
            compra.aplicar_promociones(
                supermercado.promociones.values()
            )

            supermercado.registrar_compra(compra)
            compras_realizadas.append(compra)

    return compras_realizadas, errores


##Funcion que debe usarse desde el menu.##
def ejecutar_archivo_compras(ruta, supermercado):
    with open(ruta, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    return ejecutar_compras(texto, supermercado)

