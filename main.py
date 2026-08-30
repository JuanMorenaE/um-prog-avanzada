import os
import subprocess
import pygame
import time

from Opciones import mostrar_opciones
from Juego import Juego
from Tablero import Tablero
from Vista import Vista
from Utils import Color


def limpiar_consola():
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(comando, shell=True)


tablero = Tablero()


def turnos():
    for player in tablero._players:
        yield player


def main():
    pygame.init()
    juego = Juego()
    
    while True:
        limpiar_consola()

        print("\n╔════════════════════════════╗")
        print("\tJUEGO")
        print("╚════════════════════════════╝")

        if tablero._players:
            print("\nJugadores:")
            for p in tablero._players:
                print(f"  • {p._color.name.capitalize()} - {p._name}")


        opcion = mostrar_opciones({
            "Jugar": 1,
            "Agregar jugador": 2
        })

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
                    continue

            tablero.nuevo_jugador(name,color)
            continue

        else:
            input("Opcion seleccionada inválida, presione ENTER para continuar")


    vista = Vista(tablero)

    auto_mode = mostrar_opciones({
        "Juego Automatico": True,
        "Juego Manual": False
    })

    print("Auto Mode: ", auto_mode)

    juego.auto_mode = auto_mode

    juego_terminado = False
    while not juego_terminado:
        jugadores = turnos()
        for jugador in jugadores:
            if auto_mode:
                time.sleep(1)

            limpiar_consola()

            tablero.mostrar_tablero()
            vista.dibujar()

            print("\n╔════════════════════════════════════╗")
            print(f"\tTURNO DE {jugador.nombre.upper()} ({jugador.color.name})")
            print("╚════════════════════════════════════╝")

            juego.turno_jugador(jugador)

            if jugador.es_ganador():
                print(f"\n¡{jugador.nombre} ganó la partida!")
                juego_terminado = True
                break


if __name__ == "__main__":
    main()