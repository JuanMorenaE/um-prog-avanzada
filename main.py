from Tablero import Tablero, CASILLA_FINAL

from Utils import Color
from Dados import Dados

tablero = Tablero()

tablero.nuevo_jugador("Tatu", Color.AMARILLO)
tablero.nuevo_jugador("Trive", Color.VERDE)
tablero.nuevo_jugador("Juan", Color.ROJO)

juego_terminado = False

while not juego_terminado:
    for player in tablero._players:
        print(f"\nTurno de {player._name}")

        input("\nPresioná ENTER para tirar los dados...")

        dados = Dados.tirar_dados()

        print("\n────────────────────────────────────")
        print(f"DADO: [{dados}]")
        print("────────────────────────────────────")

        print("\n¿Qué querés hacer?")

        print(f"\n[1] Sacar una ficha ({len(player._fichas)}/{player._max_fichas}).")

        if player._fichas:
            print("[2] Mover una ficha")

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
                if player.ganador(CASILLA_FINAL):
                    print(f"\n¡{player._name} ganó la partida!")
                    juego_terminado = True
                    break
            else:
                print("\n✗ No podés sacar más fichas.")

            
        elif option == 2 and player._fichas:

            print("\nTus fichas:")
            print("────────────────────────────────────")

            for i, ficha in enumerate(player._fichas):
                print(f"[{i + 1}] Posición: {ficha._posicion}.")
            
            print("────────────────────────────────────")

            fichas_validas = list(range(1, len(player._fichas) + 1))

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

            if player.ganador(CASILLA_FINAL):
                print(f"\n¡{player._name} ganó la partida!")
                juego_terminado = True
                break

        tablero.mostrar_tablero()
