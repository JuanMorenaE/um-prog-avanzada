import os
import subprocess

from Opciones import mostrar_opciones
from Juego import Juego
from Utils import Color, logDecorator, nombre_color
from Constantes import ESPERA_MODO_AUTOMATICO

juego = Juego()


def limpiar_consola():
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(comando, shell=True)


def turnos():
    for player in juego.jugadores:
        yield player

@logDecorator
def main():
    while True:
        limpiar_consola()

        print("\n╔════════════════════════════╗")
        print("\tJUEGO")
        print("╚════════════════════════════╝")

        if juego.jugadores:
            print("\nJugadores:")
            for p in juego.jugadores:
                print(f"  • {nombre_color(p.color)} - {p.nombre}")

        opciones = {}

        if len(juego.jugadores) > 1:
            opciones["Jugar"] = 1

        if len(juego.jugadores) < 4:
            opciones["Agregar jugador"] = 2

        opcion = mostrar_opciones(opciones)

        if opcion == 1:
            if len(juego.jugadores) != 0:
                print("\n¡A jugar!")
                break
            else:
                input("\nx Necesitás al menos 2 jugadores para iniciar el juego. Presioná ENTER para continuar...")
                continue

        elif opcion == 2:
            name = input("\n¿Como te llamas? > ")

            print("\nColores disponibles:")

            opciones = {}
            for color in Color:
                if juego.obtener_jugador_por_color(color) is not None:
                    continue
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
    juego.tablero.auto_mode = auto_mode
    juego.vista.iniciar()
    juego.vista.dibujar()
    
    print("Auto Mode: ", auto_mode)

    juego_terminado = False
    while not juego_terminado:
        jugadores = turnos()
        for jugador in jugadores:
            juego.vista.establecer_turno(jugador)

            if auto_mode:
                if not juego.vista.esperar(ESPERA_MODO_AUTOMATICO):
                    return

            limpiar_consola()
            if not juego.vista.dibujar():
                return

            print("\n╔════════════════════════════════════╗")
            print(f"\tTURNO DE {jugador.nombre.upper()} ({jugador.color.name})")
            print("╚════════════════════════════════════╝")

            juego.turno_jugador(jugador)

            if jugador.es_ganador():
                print(f"\n¡{jugador.nombre} ganó la partida!")
                juego.vista.mostrar_ganador(jugador)
                juego_terminado = True
                break


if __name__ == "__main__":
    main()
