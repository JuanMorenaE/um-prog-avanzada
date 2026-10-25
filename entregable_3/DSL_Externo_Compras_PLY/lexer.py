
import ply.lex as lex

# Tokens que reconoce nuestro DSL
tokens = (
    "COMPRA",
    "PRODUCTO",
    "CANTIDAD",
    "FIN",
    "ENTERO",
)

# Palabras reservadas
reservadas = {
    "COMPRA": "COMPRA",
    "PRODUCTO": "PRODUCTO",
    "CANTIDAD": "CANTIDAD",
    "FIN": "FIN",
}

# Ignorar espacios y tabulaciones
t_ignore = " \t"


# Reconocer palabras reservadas
def t_PALABRA(t):
    r"[A-Za-z_]+"

    if t.value not in reservadas:
        raise SyntaxError(
            f"Palabra desconocida: {t.value}, línea {t.lineno}"
        )

    t.type = reservadas[t.value]
    return t


# Reconocer números enteros
def t_ENTERO(t):
    r"\d+"
    t.value = int(t.value)
    return t


# Contar líneas
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Detectar caracteres inválidos
def t_error(t):
    raise SyntaxError(
        f"Carácter inválido: {t.value[0]!r}, línea {t.lineno}"
    )


# Construir el analizador léxico
lexer = lex.lex()
