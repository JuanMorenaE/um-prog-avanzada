from Clases.Supermercado import DSLSupermercado

def init():
    supermercado = DSLSupermercado()
    _ = (
        supermercado
            .producto(1)
                .nombre("Arroz")
                .precio(50)
                .categoria("Comestible")
            .producto(2)
                .nombre("Harina")
                .precio(30)
    )

    for codigo in supermercado.productos:
        print(f"{codigo} - {supermercado.productos[codigo].nombre} ${supermercado.productos[codigo].precio} - Categoria: {supermercado.productos[codigo].categoria}")

if __name__ == '__main__':
    init()