from .parser import interpretar_mantenimiento
from Clases.Producto import Producto
from Clases.Promocion import Promocion


def ejecutar_mantenimiento(texto, supermercado):
    instrucciones = interpretar_mantenimiento(texto)
    errores = []
    aplicadas = 0

    for numero, (accion, codigo, propiedades) in enumerate(instrucciones, start=1):
        try:
            match accion:
                case "add_product":
                    agregar_producto(supermercado, codigo, propiedades)
                    print(f"+ Se agregó el producto con el código {codigo}")
                case "update_product":
                    actualizar_producto(supermercado, codigo, propiedades)
                    print(f"+ Se actualizó el producto con el código {codigo}")
                case "delete_product":
                    eliminar_producto(supermercado, codigo)
                    print(f"+ Se eliminó el producto con el código {codigo}")
                case "add_offer":
                    agregar_promocion(supermercado, codigo, propiedades)
                    print(f"+ Se agregó la promoción con el código {codigo}")
                case "update_offer":
                    actualizar_promocion(supermercado, codigo, propiedades)
                    print(f"+ Se actualizó la promoción con el código {codigo}")
                case "delete_offer":
                    eliminar_promocion(supermercado, codigo)
                    print(f"+ Se eliminó la promoción con el código {codigo}")

            aplicadas += 1
        except ValueError as error:
            errores.append(f"Instruccion {numero} ({accion} {codigo}): {error}")

    return aplicadas, errores


def agregar_producto(supermercado, codigo, propiedades):
    producto = Producto(codigo)
    producto.nombre = propiedades["name"]
    producto.precio = propiedades["price"]
    producto.categoria = propiedades.get("category")
    supermercado.agregar_producto(producto)

def actualizar_producto(supermercado, codigo, propiedades):
    producto = supermercado.obtener_producto(codigo)

    nombre_anterior = producto.nombre
    precio_anterior = producto.precio
    categoria_anterior = producto.categoria

    try:
        producto.nombre = propiedades.get("name", producto.nombre)
        producto.precio = propiedades.get("price", producto.precio)
        producto.categoria = propiedades.get("category", producto.categoria)

        producto.validar()
    except ValueError:
        producto.nombre = nombre_anterior
        producto.precio = precio_anterior
        producto.categoria = categoria_anterior
        raise


def eliminar_producto(supermercado, codigo):
    supermercado.eliminar_producto(codigo)


def agregar_promocion(supermercado, codigo, propiedades):
    promocion = Promocion(codigo)
    promocion.nombre = propiedades["name"]
    promocion.descuento = propiedades["discount"]
    armar_condiciones(supermercado, promocion, propiedades.get("conditions"))
    supermercado.agregar_promocion(promocion)


def armar_condiciones(supermercado, promocion, condiciones):
    promocion.condiciones = []

    for c in condiciones:
        producto = supermercado.obtener_producto(c["codigo"])
        condicion = promocion.agregar_condicion(producto)
        condicion.operador = c["condition"]["operator"]
        condicion.cantidad = c["condition"]["quantity"]

def actualizar_promocion(supermercado, codigo, propiedades):
    promocion = supermercado.obtener_promocion(codigo)
    
    nombre_anterior = promocion.nombre
    descuento_anterior = promocion.descuento
    condiciones_anterior = promocion.condiciones

    try:
        promocion.nombre = propiedades.get("name", promocion.nombre)
        promocion.descuento = propiedades.get("discount", promocion.descuento)

        if "conditions" in propiedades:
            armar_condiciones(supermercado, promocion, propiedades.get("conditions"))

        promocion.validar()
    except ValueError:
        promocion.nombre = nombre_anterior
        promocion.descuento = descuento_anterior
        promocion.condiciones = condiciones_anterior
        raise


def eliminar_promocion(supermercado, codigo):
    supermercado.eliminar_promocion(codigo)
    

def ejecutar_archivo_mantenimiento(ruta, supermercado):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return ejecutar_mantenimiento(archivo.read(), supermercado)