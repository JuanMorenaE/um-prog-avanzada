import random

def mostrar_opciones(opciones: dict, auto_mode: bool = False):
    opciones_lista = list(opciones.items())

    print()

    for index, (nombre, valor) in enumerate(opciones_lista, start=1):
        print(f"[{index}]. {nombre}")

    opciones_validas = range(1, len(opciones_lista) + 1)

    opcion = 1

    if auto_mode:
        opcion = random.choice(opciones_validas)
    else:
        while True:
            try:
                opcion = int(input("\nOpción > "))

                if opcion in opciones_validas:
                    break

                print("Opción inválida.")
            except ValueError:
                print("Ingrese un número válido.")

    return opciones_lista[opcion - 1][1]