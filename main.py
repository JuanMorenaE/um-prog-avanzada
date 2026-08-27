import os
import subprocess

from Tablero import Tablero, CASILLA_FINAL

from Utils import Color
from Dados import Dados

def limpiar_consola():
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(comando, shell=True)

tablero = Tablero()

while True:
    limpiar_consola()

    print("\n╔════════════════════════════╗")
    print("\tJUEGO")
    print("╚════════════════════════════╝")

    if tablero._players:
        print("\nJugadores:")
        for p in tablero._players:
            print(f"  • {p._color.name.capitalize()} - {p._name}")


    print("\n\t[1] Jugar")
    print("\t[2] Agregar jugador")

    opcion = input("\nSeleccione una opción [1-2] > ")

    if opcion == "1":
        if len(tablero._players) != 0:
            print("¡A jugar!")
            break
        else:
            input("\nx Necesitás al menos un jugador para iniciar el juego. Presioná ENTER para continuar...")
            continue

    elif opcion == "2":
        name = input("¿Como te llamas? > ")

        print("\nColores disponibles:")
        for color in Color:
            print(f"\t• {color.name}")

        color = input("\nElegí tu color > ").upper()

        try:
            color = Color[color]
        except KeyError:
            input(f"\nx '{color}' no es un color válido. Presioná ENTER para continuar...")
            continue

        while tablero.buscar_jugador_por_color(color) is not None:
            print("\n x Ese color ya esta seleccionado, elegí otro color")

            print("\nColores disponibles:")
            for color in Color:
                print(f"\t• {color.name}")
    
            color = input("\nElegí otro color > ").upper()
            
            try:
                color = Color[color]
            except KeyError:
                input(f"\nx '{color}' no es un color válido...")

        tablero.nuevo_jugador(name,color)
        continue

    else:
        input("Opcion seleccionada inválida, presione ENTER para continuar")


juego_terminado = False

while not juego_terminado:
    for player in tablero._players:
        limpiar_consola()

        tablero.mostrar_tablero()

        print("\n╔════════════════════════════════════╗")
        print(f"\tTURNO DE {player._name.upper()} ({player._color.name})")
        print("╚════════════════════════════════════╝")

        input("\nPresioná ENTER para tirar los dados...")

        dados = Dados.tirar_dados()

        print(f"\n\t⚁ DADO: {dados} ⚁")

        print("\n¿Qué querés hacer?")

        print(f"\n\t[1] Sacar una ficha ({len(player._fichas)}/{player._max_fichas}).")

        if player._fichas:
            print("\t[2] Mover una ficha")

        opciones_validas = [1, 2] if player._fichas else [1]

        while True:
            try:
                option = int(input("\n> "))

                if option in opciones_validas:
                    break

                print(f"Opción inválida, selecciona una opcion disponible ({opciones_validas}) ")
            except ValueError:
                print(f"Opción inválida, selecciona una opcion disponible ({opciones_validas})")

        if option == 1:
            ficha = player.sacar_ficha()

            if ficha is not None:
                tablero._casillas[0].append(ficha)
                tablero.mover_ficha(ficha, dados)

                print(f"\n✓ Ficha movida {dados} posiciones.")
                tablero.aplicar_casilla_especial(ficha)
            else:
                print("\n✗ No podés sacar más fichas.")

            
        elif option == 2 and player._fichas:

            print("\n╔══════════════════════════╗")
            print("\tTUS FICHAS")
            print("╚══════════════════════════╝")

            fichas_validas = []

            for i, ficha in enumerate(player._fichas):
                if ficha._posicion != CASILLA_FINAL:
                    print(f"\t[{i + 1}] Posición: {ficha._posicion}")
                    fichas_validas.append(i + 1)
                else:
                    print(f"\t[{i + 1}] Posición: {ficha._posicion} (¡Llegó a la meta!)")

            while True:
                try:
                    selected_ficha = int(input("\nSeleccioná una ficha > "))

                    if selected_ficha in fichas_validas:
                        break

                    print(f"Opción inválida, selecciona una opción disponible ({fichas_validas})")
                except ValueError:
                    print(f"Opción inválida, selecciona una opción disponible ({fichas_validas})")

            ficha = player._fichas[selected_ficha - 1]
            tablero.mover_ficha(ficha, dados)

            print(f"\n✓ Ficha movida a la posicion {ficha._posicion}.")
            tablero.aplicar_casilla_especial(ficha)


        if player.ganador(CASILLA_FINAL):
            print(f"\n¡{player._name} ganó la partida!")
            juego_terminado = True
            break
