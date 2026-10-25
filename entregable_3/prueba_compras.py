from Clases.DSLSupermercado import DSLSupermercado
from DSL_Externo_Compras_PLY.parser import interpretar_compras
from DSL_Externo_Compras_PLY.ejecutor import (
    ejecutar_compras,
    ejecutar_archivo_compras,
)


def crear_supermercado():
    return (
        DSLSupermercado()
        .producto(1)
            .nombre("Harina")
            .precio(30)
        .producto(2)
            .nombre("Levadura")
            .precio(20)
        .producto(3)
            .nombre("Azucar")
            .precio(40)
        .producto(4)
            .nombre("Refresco")
            .precio(100)

        # P1: Harina + Levadura, 30%
        .promocion(1)
            .nombre("Harina y Levadura")
            .descuento(30)
            .cuando_producto(1)
            .cantidad_igual(1)
            .cuando_producto(2)
            .cantidad_igual(1)

        # P2: 2 Harinas + Azucar, 20%
        .promocion(2)
            .nombre("Harina y Azucar")
            .descuento(20)
            .cuando_producto(1)
            .cantidad_igual(2)
            .cuando_producto(3)
            .cantidad_igual(1)

        # P3: 4 Harinas, 10%
        .promocion(3)
            .nombre("Harina x4")
            .descuento(10)
            .cuando_producto(1)
            .cantidad_igual(4)

        .finalizar()
    )


def probar(nombre, texto, total_esperado=None,
           promociones_esperadas=None, errores_esperados=0):

    supermercado = crear_supermercado()

    try:
        compras, errores = ejecutar_compras(texto, supermercado)

        assert len(errores) == errores_esperados, (
            f"Se esperaban {errores_esperados} errores, "
            f"se obtuvieron {len(errores)}: {errores}"
        )

        if total_esperado is not None:
            assert len(compras) == 1, (
                f"Se esperaba 1 compra, se obtuvieron {len(compras)}"
            )

            total = compras[0].importe

            assert abs(total - total_esperado) < 0.001, (
                f"Total esperado ${total_esperado}, "
                f"obtenido ${total}"
            )

        if promociones_esperadas is not None:
            assert len(compras) == 1

            assert set(compras[0].promociones) == set(
                promociones_esperadas
            ), (
                f"Promociones esperadas: {promociones_esperadas}, "
                f"obtenidas: {compras[0].promociones}"
            )

        print(f"[OK] {nombre}")

    except Exception as error:
        print(f"[FALLO] {nombre}: {error}")
        return False

    return True


def probar_sintaxis_invalida(nombre, texto):
    try:
        interpretar_compras(texto)
        print(f"[FALLO] {nombre}: se acepto sintaxis invalida")
        return False
    except SyntaxError:
        print(f"[OK] {nombre}")
        return True
    except Exception as error:
        print(f"[FALLO] {nombre}: {error}")
        return False


if __name__ == "__main__":
    resultados = []

    # 1. Compra sin promociones
    resultados.append(probar(
        "Compra sin promociones",
        "COMPRA PRODUCTO 4 CANTIDAD 2 FIN",
        total_esperado=200,
        promociones_esperadas=[]
    ))

    # 2. Cantidad por defecto = 1
    resultados.append(probar(
        "Cantidad por defecto",
        "COMPRA PRODUCTO 4 FIN",
        total_esperado=100,
        promociones_esperadas=[]
    ))

    # 3. Promocion de varios productos
    resultados.append(probar(
        "Promocion con dos productos",
        "COMPRA PRODUCTO 1 PRODUCTO 2 FIN",
        total_esperado=35,
        promociones_esperadas=[1]
    ))

    # 4. Promociones que compiten
    # 4 harinas + levadura + azucar
    # P1 usa 1 harina y 1 levadura
    # P2 usa 2 harinas y 1 azucar
    # Queda 1 harina sin descuento
    resultados.append(probar(
        "Promociones combinadas",
        """
        COMPRA
            PRODUCTO 1 CANTIDAD 4
            PRODUCTO 2
            PRODUCTO 3
        FIN
        """,
        total_esperado=145,
        promociones_esperadas=[1, 2]
    ))

    # 5. Misma promocion aplicada dos veces
    resultados.append(probar(
        "Promocion repetida",
        "COMPRA PRODUCTO 1 CANTIDAD 8 FIN",
        total_esperado=216,
        promociones_esperadas=[3]
    ))

    # 6. Unidades sobrantes sin descuento
    resultados.append(probar(
        "Unidades sobrantes",
        "COMPRA PRODUCTO 1 CANTIDAD 5 FIN",
        total_esperado=138,
        promociones_esperadas=[3]
    ))

    # 7. Producto inexistente
    resultados.append(probar(
        "Producto inexistente",
        "COMPRA PRODUCTO 99 PRODUCTO 4 FIN",
        total_esperado=100,
        promociones_esperadas=[],
        errores_esperados=1
    ))

    # 8. Cantidad cero
    resultados.append(probar(
        "Cantidad cero",
        "COMPRA PRODUCTO 4 CANTIDAD 0 FIN",
        errores_esperados=1
    ))

    # 9. Cantidad negativa (error lexico)
    resultados.append(probar_sintaxis_invalida(
        "Cantidad negativa",
        "COMPRA PRODUCTO 4 CANTIDAD -2 FIN"
    ))

    # 10. Compra vacia
    resultados.append(probar_sintaxis_invalida(
        "Compra vacia",
        "COMPRA FIN"
    ))

    # 11. Falta FIN
    resultados.append(probar_sintaxis_invalida(
        "Falta FIN",
        "COMPRA PRODUCTO 1"
    ))

    # 12. Palabra desconocida
    resultados.append(probar_sintaxis_invalida(
        "Palabra desconocida",
        "COMPRA ARTICULO 1 FIN"
    ))

    # 13. Multiples compras
    def probar_multiples():
        supermercado = crear_supermercado()

        texto = """
        COMPRA PRODUCTO 4 FIN
        COMPRA PRODUCTO 4 CANTIDAD 2 FIN
        """

        try:
            compras, errores = ejecutar_compras(
                texto, supermercado
            )

            assert len(compras) == 2
            assert len(errores) == 0
            assert compras[0].importe == 100
            assert compras[1].importe == 200
            assert len(supermercado.compras) == 2

            print("[OK] Multiples compras")
            return True

        except Exception as error:
            print(f"[FALLO] Multiples compras: {error}")
            return False

    resultados.append(probar_multiples())

    # 14. Operador >=
    def probar_mayor_igual():
        supermercado = (
            DSLSupermercado()
            .producto(1)
                .nombre("Harina")
                .precio(30)
            .promocion(1)
                .nombre("Harina x3 o mas")
                .descuento(20)
                .cuando_producto(1)
                .cantidad_mayor_igual(3)
            .finalizar()
        )

        try:
            compras, errores = ejecutar_compras(
                "COMPRA PRODUCTO 1 CANTIDAD 4 FIN",
                supermercado
            )

            assert not errores
            assert len(compras) == 1
            assert compras[0].importe == 102

            print("[OK] Operador >=")
            return True

        except Exception as error:
            print(f"[FALLO] Operador >=: {error}")
            return False

    resultados.append(probar_mayor_igual())


    # 15. Lectura de compras desde archivo
    def probar_archivo():
        supermercado = crear_supermercado()

        try:
            compras, errores = ejecutar_archivo_compras(
                "entregable_3/DSL_Externo_Compras_PLY/compras.txt",
                supermercado
            )

            assert len(compras) == 3
            assert len(errores) == 0

            assert compras[0].importe == 145
            assert compras[1].importe == 216
            assert compras[2].importe == 200

            assert len(supermercado.compras) == 3

            print("[OK] Lectura desde archivo TXT")
            return True

        except Exception as error:
            print(f"[FALLO] Lectura desde archivo TXT: {error}")
            return False

    resultados.append(probar_archivo())


    # 16. Recuperación de errores sintácticos
    def probar_recuperacion_sintactica():
        supermercado = crear_supermercado()

        texto = """
        COMPRA
            PRODUCTO 4
        FIN

        COMPRA
            PRODUCTO 1 CANTIDAD
        FIN

        COMPRA
            PRODUCTO 4 CANTIDAD 2
        FIN
        """

        try:
            compras, errores = ejecutar_compras(
                texto, supermercado
            )

            assert len(compras) == 2, (
                f"Se esperaban 2 compras, "
                f"se obtuvieron {len(compras)}"
            )

            assert compras[0].importe == 100
            assert compras[1].importe == 200

            assert len(errores) == 1, (
                f"Se esperaba 1 error, "
                f"se obtuvieron {len(errores)}: {errores}"
            )

            assert len(supermercado.compras) == 2

            print("[OK] Recuperacion de errores sintacticos")
            return True

        except Exception as error:
            print(
                f"[FALLO] Recuperacion sintactica: {error}"
            )
            return False

    resultados.append(probar_recuperacion_sintactica())



    # RESUMEN
    aprobadas = sum(resultados)
    total = len(resultados)

    print("\n" + "=" * 40)
    print(f"RESULTADO: {aprobadas}/{total} pruebas aprobadas")
    print("=" * 40)

    if aprobadas != total:
        raise SystemExit(1)
