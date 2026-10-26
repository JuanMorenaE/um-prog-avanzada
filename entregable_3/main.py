from Clases.DSLSupermercado import DSLSupermercado
from DSL_Externo_Compras_PLY.ejecutor import ejecutar_archivo_compras
from DSL_Externo_Mantenimiento_Lark.ejecutor import ejecutar_archivo_mantenimiento
from pathlib import Path
from pprint import pprint


def init():
    supermercado = (
        DSLSupermercado()
            .producto(1)
                .nombre("Arroz")
                .precio(50)
                .categoria("Comestible")
            .producto(2)
                .nombre("Harina")
                .precio(30)
            .producto(3)
                .categoria("Bebida")
                .precio(100)
                .nombre("Refresco")
            .promocion(1)
                .nombre("Harina x5")
                .cuando_producto(2)
                    .cantidad_mayor_igual(5)
                .descuento(20)
            .producto(4)
                .precio(150)
                .nombre("Pizza")
            .promocion(2)
                .descuento(25)
                .cuando_producto(3)
                .cuando_producto(4)
                    .cantidad_igual(2)
                .nombre("2 pizzas + refresco")
            .finalizar()
    )

    show_menu(supermercado)

def show_menu(supermercado):
    while True:
        print()
        print("===========================================")
        print("             MENU PRINCIPAL                ")
        print("===========================================")
        print()
        print(" 1. Mantenimiento de productos y promociones")
        print(" 2. Realizar compras")
        print(" 3. Ver la lista de productos")
        print(" 4. Ver la lista de promociones")
        print(" 5. Ver la lista de compras")
        print(" 6. Salir")
        print()

        try:
            opcion = int(input("> Opcion: "))
        except ValueError:
            print("Opcion invalida. Intente nuevamente.")
            continue

        match opcion:
            case 1:
                mantenimiento(supermercado)
            case 2:
                compras(supermercado)
            case 3:
                imprimir_lista_productos(supermercado)
            case 4:
                imprimir_lista_promociones(supermercado)
            case 5:
                imprimir_lista_compras(supermercado)
            case 6:
                exit()
            case _:
                print("Opcion invalida. Intente nuevamente.")


def mantenimiento(supermercado):
    ruta = Path(__file__).resolve().parent / "mantenimiento.txt"
    try:
        print()
        aplicadas, errores = ejecutar_archivo_mantenimiento(ruta, supermercado)
    except FileNotFoundError:
        print("No se encontro el archivo")
        return
    except (OSError, UnicodeError) as error:
        print(f"No se pudo leer el archivo de mantenimiento: {error}")
        return
    except Exception as error:
        # El parser de mantenimiento comunica los errores sintacticos como Exception.
        print(f"No se pudo ejecutar el mantenimiento: {error}")
        return

    print(f"\nInstrucciones aplicadas: {aplicadas}")
    if errores:
        print("\nErrores:")
        for error in errores:
            print(" -", error)
    


def compras(supermercado):
    ruta = Path(__file__).resolve().parent / "compras.txt"
    try:
        compras_realizadas, errores = ejecutar_archivo_compras(ruta, supermercado)
    except (OSError, UnicodeError) as error:
        print(f"No se pudo leer el archivo de compras: {error}")
        return

    for compra in compras_realizadas:
        print()
        print(compra)

    print(f"\nCompras registradas: {len(compras_realizadas)}")
    if errores:
        print("\nErrores:")
        for error in errores:
            print(" -", error)


def imprimir_lista_compras(supermercado):
    print()
    print("===========================================")
    print("                  COMPRAS                  ")
    print("===========================================")
    if not supermercado.compras:
        print("Todavia no existen compras registradas.")
        return

    for compra in supermercado.compras:
        print()
        print(compra)


def imprimir_lista_productos(supermercado):
    print()
    print("===========================================")
    print("                 PRODUCTOS                 ")
    print("===========================================")
    print()
    for producto in supermercado.productos.values():
        print(producto)

def imprimir_lista_promociones(supermercado):
    print()
    print("===========================================")
    print("               PROMOCIONES                 ")
    print("===========================================")
    print()
    for promocion in supermercado.promociones.values():
        print(promocion)

if __name__ == '__main__':
    init()
