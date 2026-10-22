from Clases.DSLSupermercado import DSLSupermercado

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

        opcion = int(input("> Opcion: "))

        match opcion:
            case 3:
                imprimir_lista_productos(supermercado)
            case 4:
                imprimir_lista_promociones(supermercado)
            case 6:
                exit()


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