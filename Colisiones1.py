import numpy as np
from Aestrella import AEstrella

# Definir el tablero (como en el código anterior)
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
    """Obtiene las coordenadas de las casillas según los números dados"""
    coordenadas = []
    for num in numeros:
        resultado = np.where(tablero == num)
        if len(resultado[0]) > 0:
            coordenadas.append((resultado[0][0], resultado[1][0]))  # Devuelve la coordenada (fila, columna)
    return coordenadas

def menu():
    while True:
        print("\nMenú:")
        print("1. Ingresar objetivo para Montacargas 1")
        print("2. Ingresar objetivo para Montacargas 2")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")

        # Ingresar el objetivo para Montacargas 1
        if opcion == "1":
            objetivo_1 = int(input("Ingrese el número de la casilla objetivo para Montacargas 1 (1-48): "))
            if objetivo_1 < 1 or objetivo_1 > 48:
                print("Número de objetivo inválido, debe estar entre 1 y 48.")
                continue

            objetivo_1_coord = obtener_coordenadas(tablero, [objetivo_1])
            if not objetivo_1_coord:
                print(f"Objetivo {objetivo_1} no es válido. Intente nuevamente.")
                continue

        # Ingresar el objetivo para Montacargas 2
        elif opcion == "2":
            objetivo_2 = int(input("Ingrese el número de la casilla objetivo para Montacargas 2 (1-48): "))
            if objetivo_2 < 1 or objetivo_2 > 48:
                print("Número de objetivo inválido, debe estar entre 1 y 48.")
                continue

            objetivo_2_coord = obtener_coordenadas(tablero, [objetivo_2])
            if not objetivo_2_coord:
                print(f"Objetivo {objetivo_2} no es válido. Intente nuevamente.")
                continue

        # Salir del programa
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción inválida")
            continue

        # Si ambos objetivos son válidos, procesamos los caminos
        montacargas_1 = AEstrella(tablero)
        montacargas_2 = AEstrella(tablero)

        # Obtener los caminos de ambos montacargas
        camino_1, costo_1 = montacargas_1.calcular_ruta_con_costos(montacargas_1.inicio, objetivo_1_coord[0])
        camino_2, costo_2 = montacargas_2.calcular_ruta_con_costos(montacargas_2.inicio, objetivo_2_coord[0])

        # Verificar si ambos caminos son válidos
        if camino_1 is None or camino_2 is None:
            print("No se pudo encontrar un camino para uno de los montacargas.")
            continue

        print(f"Camino Montacargas 1: {camino_1}, Costo: {costo_1}")
        print(f"Camino Montacargas 2: {camino_2}, Costo: {costo_2}")

        # Graficar los caminos de ambos montacargas
        montacargas_1.graficar_camino([camino_1], [objetivo_1])
        montacargas_2.graficar_camino([camino_2], [objetivo_2])

menu()
