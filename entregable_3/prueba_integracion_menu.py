import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import main


BASE = Path(__file__).resolve().parent


class PruebasIntegracionMenu(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory(prefix="supermercado pruebas ")
        self.addCleanup(temporal.cleanup)
        self.directorio = Path(temporal.name)

    def ejecutar_menu(self, opciones, texto_compras=None, texto_mantenimiento=None):
        for nombre, contenido in (
            ("compras.txt", texto_compras),
            ("mantenimiento.txt", texto_mantenimiento),
        ):
            if contenido is not None:
                ruta = self.directorio / nombre
                if isinstance(contenido, bytes):
                    ruta.write_bytes(contenido)
                else:
                    ruta.write_text(contenido, encoding="utf-8")

        salida = io.StringIO()
        supermercados = []
        menu_original = main.show_menu

        def observar_menu(supermercado):
            supermercados.append(supermercado)
            menu_original(supermercado)

        with (
            patch.object(main, "__file__", str(self.directorio / "main.py")),
            patch.object(main, "show_menu", side_effect=observar_menu),
            patch("builtins.input", side_effect=opciones),
            patch("sys.stdout", salida),
        ):
            with self.assertRaises(SystemExit) as finalizacion:
                main.init()

        self.assertIn(finalizacion.exception.code, (None, 0))
        self.assertEqual(len(supermercados), 1)
        return supermercados[0], salida.getvalue()

    def test_listados_opciones_invalidas_y_salida(self):
        supermercado, salida = self.ejecutar_menu(
            ["5", "3", "4", "abc", "99", "6"]
        )
        self.assertIn("MENU PRINCIPAL", salida)
        self.assertIn("Todavia no existen compras registradas.", salida)
        self.assertIn("Arroz", salida)
        self.assertIn("Harina x5", salida)
        self.assertEqual(salida.count("Opcion invalida"), 2)
        self.assertEqual(len(supermercado.productos), 4)
        self.assertEqual(len(supermercado.promociones), 2)
        self.assertEqual(supermercado.compras, [])

    def test_compras_repetidas_acumulan_sin_doble_registro(self):
        texto = (BASE / "compras.txt").read_text(encoding="utf-8")
        supermercado, salida = self.ejecutar_menu(
            ["2", "5", "2", "5", "6"], texto_compras=texto
        )
        self.assertEqual(
            [compra.importe for compra in supermercado.compras],
            [330, 400, 300, 330, 400, 300],
        )
        self.assertEqual(salida.count("Compras registradas: 3"), 2)
        self.assertIn("TOTAL: $330.00", salida)

    def test_mantenimiento_comparte_precios_promociones_e_historial(self):
        mantenimiento = '''
ACTUALIZAR PRODUCTO 2 PRECIO 40 FIN
ACTUALIZAR PROMOCION 1 DESCUENTO 10 FIN
'''
        supermercado, salida = self.ejecutar_menu(
            ["2", "1", "2", "5", "6"],
            texto_compras="COMPRA PRODUCTO 2 CANTIDAD 5 FIN",
            texto_mantenimiento=mantenimiento,
        )
        self.assertEqual(supermercado.productos[2].precio, 40)
        self.assertEqual(supermercado.promociones[1].descuento, 10)
        self.assertEqual(
            [compra.importe for compra in supermercado.compras], [120, 180]
        )
        self.assertEqual(supermercado.compras[0].productos[0]["precio"], 30)
        self.assertEqual(supermercado.compras[0].productos[0]["descuento"], 20)
        self.assertIn("Instrucciones aplicadas: 2", salida)
        self.assertIn("TOTAL: $180.00", salida)

    def test_mantenimiento_de_ejemplo_y_producto_eliminado(self):
        supermercado, salida = self.ejecutar_menu(
            ["1", "2", "5", "6"],
            texto_compras=(BASE / "compras.txt").read_text(encoding="utf-8"),
            texto_mantenimiento=(BASE / "mantenimiento.txt").read_text(encoding="utf-8"),
        )
        self.assertNotIn(1, supermercado.productos)
        self.assertIn(5, supermercado.productos)
        self.assertIn(6, supermercado.productos)
        self.assertEqual(
            [compra.importe for compra in supermercado.compras], [135.5, 300]
        )
        self.assertIn("Instrucciones aplicadas: 8", salida)
        self.assertIn("No existe un producto con el codigo 1", salida)

    def test_producto_agregado_por_mantenimiento_se_puede_comprar(self):
        supermercado, salida = self.ejecutar_menu(
            ["1", "2", "5", "6"],
            texto_mantenimiento='AGREGAR PRODUCTO 5 NOMBRE "Azúcar" PRECIO 60 FIN',
            texto_compras="COMPRA PRODUCTO 5 CANTIDAD 2 FIN",
        )
        self.assertEqual(len(supermercado.compras), 1)
        self.assertEqual(supermercado.compras[0].importe, 120)
        self.assertIn("Azúcar x2", salida)

    def test_archivos_inexistentes_no_cierran_menu(self):
        supermercado, salida = self.ejecutar_menu(["1", "2", "5", "6"])
        self.assertIn("No se encontro el archivo", salida)
        self.assertIn("No se pudo leer el archivo de compras", salida)
        self.assertEqual(supermercado.compras, [])

    def test_compras_vacias_no_cierran_menu(self):
        supermercado, salida = self.ejecutar_menu(
            ["2", "5", "6"], texto_compras=""
        )
        self.assertEqual(supermercado.compras, [])
        self.assertIn("Compras registradas: 0", salida)

    def test_errores_sintacticos_y_semanticos_conservan_compras_validas(self):
        texto = '''
COMPRA PRODUCTO 3 FIN
COMPRA PRODUCTO 2 CANTIDAD FIN
COMPRA PRODUCTO 99 PRODUCTO 2 CANTIDAD 0 PRODUCTO 4 FIN
COMPRA PRODUCTO 3 CANTIDAD 2 FIN
'''
        supermercado, salida = self.ejecutar_menu(
            ["2", "5", "6"], texto_compras=texto
        )
        self.assertEqual(
            [compra.importe for compra in supermercado.compras], [100, 150, 200]
        )
        self.assertIn("Error sintáctico", salida)
        self.assertIn("No existe un producto con el codigo 99", salida)
        self.assertIn("cantidad inválida", salida)
        self.assertIn("Compras registradas: 3", salida)

    def test_errores_de_codificacion_no_cierran_menu(self):
        supermercado, salida = self.ejecutar_menu(
            ["1", "2", "5", "6"],
            texto_compras=b"\xff",
            texto_mantenimiento=b"\xff",
        )
        self.assertIn("No se pudo leer el archivo de mantenimiento", salida)
        self.assertIn("No se pudo leer el archivo de compras", salida)
        self.assertEqual(supermercado.compras, [])

    def test_error_sintactico_de_mantenimiento_no_cierra_menu(self):
        supermercado, salida = self.ejecutar_menu(
            ["1", "2", "5", "6"],
            texto_mantenimiento="AGREGAR PRODUCTO FIN",
            texto_compras="COMPRA PRODUCTO 1 FIN",
        )
        self.assertIn("No se pudo ejecutar el mantenimiento", salida)
        self.assertEqual(len(supermercado.compras), 1)
        self.assertEqual(supermercado.compras[0].importe, 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
