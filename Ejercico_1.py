import numpy as np
import matplotlib.pyplot as plt
from Aestrella import AEstrella

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

def menu():
    while True:
        print("\nMenú:")
        print("1. Ingresar un solo objetivo")
        print("2. Ingresar múltiples objetivos")
        print("3. Ingresar objetivos y un punto de inicio distinto")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            objetivo = int(input("Ingrese el número de la casilla objetivo: "))
            objetivos = obtener_coordenadas(tablero, [objetivo])
            objetivos_numeros = [objetivo]
            a_estrella = AEstrella(tablero)
        
        elif opcion == "2":
            objetivos_numeros = list(map(int, input("Ingrese los números de las casillas objetivo separados por espacios: ").split()))
            objetivos = obtener_coordenadas(tablero, objetivos_numeros)
            a_estrella = AEstrella(tablero)
        
        elif opcion == "3":
            inicio = tuple(map(int, input("Ingrese la coordenada del punto de inicio (fila, columna): ").split(',')))
            objetivos_numeros = list(map(int, input("Ingrese los números de las casillas objetivo separados por espacios: ").split()))
            objetivos = obtener_coordenadas(tablero, objetivos_numeros)
            a_estrella = AEstrella(tablero, inicio)
        
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción inválida")
            continue

        caminos, costo = a_estrella.buscar_camino(objetivos)
        print("Camino encontrado:", [list(map(tuple, camino)) for camino in caminos])
        print("Costo total:", costo)
        a_estrella.graficar_camino(caminos, objetivos_numeros)

menu()
