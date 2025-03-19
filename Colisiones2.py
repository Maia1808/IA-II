import numpy as np
from Aestrella2 import AEstrella

##Solo un monta cargas cambia su ruta ante una solición, el que tiene el menor costo de cambiarla 

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
    coordenadas = []
    for num in numeros:
        resultado = np.where(tablero == num)
        if len(resultado[0]) > 0:
            coordenadas.append((resultado[0][0], resultado[1][0]))
    return coordenadas

def menu():
    while True:
        print("\nMenú:")
        print("1. Ingresar objetivo para Montacargas 1")
        print("2. Ingresar objetivo para Montacargas 2")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            objetivo_1 = int(input("Ingrese el número de la casilla objetivo para Montacargas 1: "))
            objetivo_1_coord = obtener_coordenadas(tablero, [objetivo_1])[0]
            montacargas_1 = AEstrella(tablero)
            camino_1, costo_1 = montacargas_1.calcular_ruta_con_costos(montacargas_1.inicio, objetivo_1_coord)
            print(f"Camino Montacargas 1: {camino_1}, Costo: {costo_1}")
            montacargas_1.graficar_camino([camino_1], [objetivo_1])
        
        elif opcion == "2":
            objetivo_2 = int(input("Ingrese el número de la casilla objetivo para Montacargas 2: "))
            objetivo_2_coord = obtener_coordenadas(tablero, [objetivo_2])[0]
            montacargas_2 = AEstrella(tablero)
            camino_2, costo_2 = montacargas_2.calcular_ruta_con_costos(montacargas_2.inicio, objetivo_2_coord)
            print(f"Camino Montacargas 2: {camino_2}, Costo: {costo_2}")
            montacargas_2.graficar_camino([camino_2], [objetivo_2])
        
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción inválida")
            continue

menu()
