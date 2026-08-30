import os
import subprocess
import pygame
import time

from Opciones import mostrar_opciones
from Juego import Juego
from Tablero import Tablero
from Vista import Vista
from Utils import Color

juego = Juego()


def limpiar_consola():
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(comando, shell=True)


def turnos():
    for player in juego.jugadores:
        yield player


def main():
    pygame.init()
    
    while True:
        limpiar_consola()

        print("\n╔════════════════════════════╗")
        print("\tJUEGO")
        print("╚════════════════════════════╝")

        if juego.jugadores:
            print("\nJugadores:")
            for p in juego.jugadores:
                print(f"  • {p.color.name.capitalize()} - {p.nombre}")


        opcion = mostrar_opciones({
            "Jugar": 1,
            "Agregar jugador": 2
        })

        if opcion == 1:
            if len(juego.jugadores) != 0:
                print("\n¡A jugar!")
                break
            else:
                input("\nx Necesitás al menos un jugador para iniciar el juego. Presioná ENTER para continuar...")
                continue

        elif opcion == 2:
            name = input("\n¿Como te llamas? > ")

            print("\nColores disponibles:")

            opciones = {}
            for color in Color:
                opciones[f"{color.name}"] = color

            color = mostrar_opciones(opciones)

            while juego.obtener_jugador_por_color(color) is not None:
                print("\n x Ese color ya esta seleccionado, elegí otro color")

                print("\nColores disponibles:")
                
                opciones = {}
                for color in Color:
                    opciones[f"{color.name}"] = color
    
                color = mostrar_opciones(opciones)

            juego.nuevo_jugador(name, color)
            continue

        else:
            input("Opcion seleccionada inválida, presione ENTER para continuar")

    auto_mode = mostrar_opciones({
        "Juego Automatico": True,
        "Juego Manual": False
    })
    juego.auto_mode = auto_mode
    print("Auto Mode: ", auto_mode)

    juego_terminado = False
    while not juego_terminado:
        jugadores = turnos()
        for jugador in jugadores:
            if auto_mode:
                time.sleep(1)

            limpiar_consola()
            juego.vista.dibujar()

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