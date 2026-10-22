from Clases.Supermercado import DSLSupermercado

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
        print("1. Mantenimiento de productos y promociones")
        print("2. Realizar compras")
        print("3. Ver la lista de productos")
        print("4. Ver la lista de promociones")
        print("5. Ver la lista de compras")
        print("6. Salir")

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
    for codigo in supermercado.productos:
        produto = supermercado.productos[codigo]
        print(f"{codigo} - {produto}")

def imprimir_lista_promociones(supermercado):
    print()
    for codigo in supermercado.promociones:
        promocion = supermercado.promociones[codigo]
        print(promocion)

if __name__ == '__main__':
    init()