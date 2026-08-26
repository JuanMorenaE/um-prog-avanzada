from Tablero import Tablero

from Utils import Color
from Dados import Dados

tablero = Tablero()

tablero.new_player("Tatu", Color.AMARILLO)
tablero.new_player("Trive", Color.VERDE)
tablero.new_player("Juan", Color.ROJO)

while True:
    for player in tablero._players:
        print(f"\nTurno de {player._name}")

        input("\nPresioná ENTER para tirar los dados...")

        dados = Dados.tirar_dados()

        print("\n────────────────────────────────────")
        print(f"DADO: [{dados}]")
        print("────────────────────────────────────")

        print("\n¿Qué querés hacer?")

        print(f"\n[1] Sacar una ficha ({len(player._fichas)}/{player._max_fichas}).")
        print("[2] Mover una ficha")

        option = int(input("\n> "))

        if option == 1:
            ficha = player.sacar_ficha()

            if ficha is not None:
                tablero._casillas[0].append(ficha)
                tablero.mover_ficha(ficha, dados)

                print(f"\n✓ Ficha movida {dados} posiciones.")
            else:
                print("\n✗ No podés sacar más fichas.")

            
        elif option == 2:
            print("\nTus fichas:")
            print("────────────────────────────────────")

            for i, ficha in enumerate(player._fichas):
                print(f"[{i + 1}] Posición: {ficha._posicion}.")
            
            print("────────────────────────────────────")

            selected_ficha = int(input("\nSeleccioná una ficha > "))

            ficha = player._fichas[selected_ficha - 1]
            tablero.mover_ficha(ficha, dados)

            print(f"\n✓ Ficha movida a la posicion {ficha._posicion}.")

        tablero.mostrar_tablero()