
import ply.yacc as yacc

try:
    from .lexer import tokens, lexer
except ImportError:
    from lexer import tokens, lexer


# ---------------------------------
# REGLAS GRAMATICALES
# ---------------------------------

def p_compras_multiples(p):
    "compras : compras compra"
    p[0] = p[1] + [p[2]]


def p_compras_unica(p):
    "compras : compra"
    p[0] = [p[1]]


def p_compra(p):
    "compra : COMPRA productos FIN"
    p[0] = p[2]


def p_productos_multiples(p):
    "productos : productos producto"
    p[0] = p[1] + [p[2]]


def p_productos_unico(p):
    "productos : producto"
    p[0] = [p[1]]


def p_producto_con_cantidad(p):
    "producto : PRODUCTO ENTERO CANTIDAD ENTERO"
    p[0] = (p[2], p[4])


def p_producto_sin_cantidad(p):
    "producto : PRODUCTO ENTERO"
    p[0] = (p[2], 1)


# ---------------------------------
# MANEJO DE ERRORES SINTÁCTICOS
# ---------------------------------

def p_error(p):
    if p:
        raise SyntaxError(
            f"Error sintáctico en {p.value!r}, línea {p.lineno}"
        )

    raise SyntaxError("Entrada incompleta")


# ---------------------------------
# CONSTRUCCIÓN DEL PARSER
# ---------------------------------

parser = yacc.yacc(
    start="compras",
    write_tables=False
)


# ---------------------------------
# FUNCIONES DE INTERPRETACIÓN
# ---------------------------------

def interpretar_compras(texto):
    lexer.lineno = 1
    return parser.parse(texto, lexer=lexer)


def interpretar_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    return interpretar_compras(texto)


def separar_compras(texto):
    bloques = []
    errores = []

    inicio = None
    lineas = texto.splitlines()

    for numero_linea, linea in enumerate(lineas, start=1):
        palabras = linea.strip().split()

        # Detectar el comienzo de una compra
        if palabras and palabras[0] == "COMPRA":
            if inicio is not None:
                errores.append(
                    f"Línea {inicio}: compra sin FIN"
                )

            inicio = numero_linea

        # Detectar el final de una compra
        if palabras and palabras[-1] == "FIN":
            if inicio is None:
                errores.append(
                    f"Línea {numero_linea}: FIN sin COMPRA"
                )
            else:
                bloque = "\n".join(
                    lineas[inicio - 1:numero_linea]
                )

                bloques.append((inicio, bloque))
                inicio = None

    if inicio is not None:
        errores.append(
            f"Línea {inicio}: compra sin FIN"
        )

    return bloques, errores


def interpretar_compras_con_errores(texto):
    bloques, errores = separar_compras(texto)
    compras = []

    for linea_inicio, bloque in bloques:
        try:
            resultado = interpretar_compras(bloque)
            compras.extend(resultado)

        except SyntaxError as error:
            errores.append(
                f"Línea {linea_inicio}: {error}"
            )

    return compras, errores



# ---------------------------------
# PRUEBA DEL PARSER
# ---------------------------------

if __name__ == "__main__":
    from DSL import data

    resultado = interpretar_compras(data)

    for numero, compra in enumerate(resultado, start=1):
        print(f"Compra {numero}: {compra}")
