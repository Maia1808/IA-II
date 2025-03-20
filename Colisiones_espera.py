import numpy as np
import matplotlib.pyplot as plt
from Aestrella2 import AEstrella

# Definir el tablero (todas las casillas por donde se puede mover son 0)
tablero = np.array([
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  1,  2,  0,  0,  9, 10,  0,  0, 17, 18,  0],
    [ 0,  0,  3,  4,  0,  0, 11, 12,  0,  0, 19, 20,  0],
    [ 0,  0,  5,  6,  0,  0, 13, 14,  0,  0, 21, 22,  0],
    [ 0,  0,  7,  8,  0,  0, 15, 16,  0,  0, 23, 24,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0, 25, 26,  0,  0, 33, 34,  0,  0, 41, 42,  0],
    [ 0,  0, 27, 28,  0,  0, 35, 36,  0,  0, 43, 44,  0],
    [ 0,  0, 29, 30,  0,  0, 37, 38,  0,  0, 45, 46,  0],
    [ 0,  0, 31, 32,  0,  0, 39, 40,  0,  0, 47, 48,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
])

def obtener_coordenadas(tablero, numeros):
    coordenadas = []
    for num in numeros:
        resultado = np.where(tablero == num)
        if len(resultado[0]) > 0:
            coordenadas.append((resultado[0][0], resultado[1][0]))
    return coordenadas

def detectar_colision(paso1, paso2):
    return paso1 == paso2  # Si las siguientes posiciones coinciden, hay colisión

def menu():
    caminos1 = None
    caminos2 = None
    objetivos1_numeros = []
    objetivos2_numeros = []

    while True:
        print("\nMenú:")
        print("1. Ingresar objetivos para ambos montacargas")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            # Ingresar objetivos para el primer montacargas
            tipo_objetivo1 = input("¿Va a ingresar un solo objetivo o varios para el primer montacargas? (1 para uno, 2 para varios): ")
            if tipo_objetivo1 == "1":
                objetivo1 = int(input("Ingrese el número de la casilla objetivo para el primer montacargas: "))
                objetivos1 = obtener_coordenadas(tablero, [objetivo1])
                objetivos1_numeros = [objetivo1]
            elif tipo_objetivo1 == "2":
                objetivos1_numeros = list(map(int, input("Ingrese los números de las casillas objetivo para el primer montacargas separados por espacios: ").split()))
                objetivos1 = obtener_coordenadas(tablero, objetivos1_numeros)
            else:
                print("Opción inválida. Intente nuevamente.")
                continue

            # Ingresar objetivos para el segundo montacargas
            tipo_objetivo2 = input("¿Va a ingresar un solo objetivo o varios para el segundo montacargas? (1 para uno, 2 para varios): ")
            if tipo_objetivo2 == "1":
                objetivo2 = int(input("Ingrese el número de la casilla objetivo para el segundo montacargas: "))
                objetivos2 = obtener_coordenadas(tablero, [objetivo2])
                objetivos2_numeros = [objetivo2]
            elif tipo_objetivo2 == "2":
                objetivos2_numeros = list(map(int, input("Ingrese los números de las casillas objetivo para el segundo montacargas separados por espacios: ").split()))
                objetivos2 = obtener_coordenadas(tablero, objetivos2_numeros)
            else:
                print("Opción inválida. Intente nuevamente.")
                continue

            # Calcular los caminos para ambos montacargas
            a_estrella1 = AEstrella(tablero)
            caminos1, costo1 = a_estrella1.buscar_camino(objetivos1)
            print("Camino encontrado para el primer montacargas:", caminos1)

            a_estrella2 = AEstrella(tablero, inicio=(6, 0))
            caminos2, costo2 = a_estrella2.buscar_camino(objetivos2)
            print("Camino encontrado para el segundo montacargas:", caminos2)

        elif opcion == "2":
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción inválida")
            continue

        # Simulación del movimiento simultáneo de ambos montacargas
        i = 0
        en_espera1 = False  # Estado de espera del montacargas 1

        while i < min(len(caminos1[0]), len(caminos2[0])):
            siguiente_pos1 = caminos1[0][i+1] if i+1 < len(caminos1[0]) else None
            siguiente_pos2 = caminos2[0][i+1] if i+1 < len(caminos2[0]) else None

            if siguiente_pos1 and siguiente_pos2 and detectar_colision(siguiente_pos1, siguiente_pos2):
                print(f"Colisión detectada en el paso {i+1}!")
                if not en_espera1:
                    # El montacargas 1 entra en espera
                    en_espera1 = True
                    print(f"Montacargas 1 espera en la casilla {caminos1[0][i]}")
                # El montacargas 2 sigue su camino normalmente
                print(f"Montacargas 2 está en: {caminos2[0][i]}")
            else:
                # Si el montacargas 1 no está en espera, mueve
                if not en_espera1:
                    print(f"Montacargas 1 está en: {caminos1[0][i]}")
                    # Verificamos si el montacargas 1 puede moverse
                    siguiente_pos1 = caminos1[0][i+1] if i+1 < len(caminos1[0]) else None
                    if siguiente_pos1:
                        print(f"Montacargas 1 se mueve a {siguiente_pos1}")
                else:
                    # Si está en espera, no mueve y mantiene su posición
                    en_espera1 = False  # Termina el turno de espera
                    print(f"Montacargas 1 sigue esperando en {caminos1[0][i]}")

                # El montacargas 2 se mueve normalmente
                print(f"Montacargas 2 se mueve a: {caminos2[0][i]}")

            i += 1
        
        a_estrella1.graficar_camino(caminos1, objetivos1_numeros)
        a_estrella2.graficar_camino(caminos2, objetivos2_numeros)

menu()
