import numpy as np
import matplotlib.pyplot as plt
from Aestrella2 import AEstrella
import matplotlib.animation as animation

# Definir el tablero (todas las casillas por donde se puede mover son 0)
tablero = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0, 9, 10, 0, 0, 17, 18, 0],
    [0, 0, 3, 4, 0, 0, 11, 12, 0, 0, 19, 20, 0],
    [0, 0, 5, 6, 0, 0, 13, 14, 0, 0, 21, 22, 0],
    [0, 0, 7, 8, 0, 0, 15, 16, 0, 0, 23, 24, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 25, 26, 0, 0, 33, 34, 0, 0, 41, 42, 0],
    [0, 0, 27, 28, 0, 0, 35, 36, 0, 0, 43, 44, 0],
    [0, 0, 29, 30, 0, 0, 37, 38, 0, 0, 45, 46, 0],
    [0, 0, 31, 32, 0, 0, 39, 40, 0, 0, 47, 48, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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

def recalcular_ruta(tablero, objetivos, montacargas_inicio, obstaculo_pos):
    tablero_con_obstaculo = np.copy(tablero)
    tablero_con_obstaculo[obstaculo_pos] = 1  # Convertir la casilla de colisión en obstáculo
    a_estrella = AEstrella(tablero_con_obstaculo, inicio=montacargas_inicio)
    caminos, costo = a_estrella.buscar_camino(objetivos)
    return caminos, costo, a_estrella

def animar_caminos(caminos1, caminos2, tablero):
    fig, ax = plt.subplots()
    ax.set_xlim(0, tablero.shape[1])
    ax.set_ylim(0, tablero.shape[0])
    plt.gca().invert_yaxis()

    # Dibujar la cuadrícula
    for i in range(tablero.shape[0] + 1):
        ax.axhline(i, color='black', lw=1)
    for j in range(tablero.shape[1] + 1):
        ax.axvline(j, color='black', lw=1)

    # Numerar las casillas con obstáculos
    for i in range(tablero.shape[0]):
        for j in range(tablero.shape[1]):
            if tablero[i, j] != 0:
                ax.text(j + 0.5, i + 0.5, str(tablero[i, j]), ha='center', va='center', fontsize=10, color='black')

    # Inicializar los puntos de los montacargas
    punto1, = ax.plot([], [], 'bo', markersize=10, label="Montacargas 1")
    punto2, = ax.plot([], [], 'ro', markersize=10, label="Montacargas 2")

    # Listas para almacenar los parches de los caminos
    camino1_parches = []
    camino2_parches = []

    def init():
        punto1.set_data([], [])
        punto2.set_data([], [])
        return punto1, punto2

    def animate(i):
        # Dibujar el camino recorrido por el Montacargas 1
        if i < len(caminos1[0]):
            x1, y1 = caminos1[0][i]
            punto1.set_data([y1 + 0.5], [x1 + 0.5])
            # Pintar la casilla recorrida por el Montacargas 1
            rect1 = plt.Rectangle((y1, x1), 1, 1, color='blue', alpha=0.3)
            ax.add_patch(rect1)
            camino1_parches.append(rect1)

        # Dibujar el camino recorrido por el Montacargas 2
        if i < len(caminos2[0]):
            x2, y2 = caminos2[0][i]
            punto2.set_data([y2 + 0.5], [x2 + 0.5])
            # Pintar la casilla recorrida por el Montacargas 2
            rect2 = plt.Rectangle((y2, x2), 1, 1, color='red', alpha=0.3)
            ax.add_patch(rect2)
            camino2_parches.append(rect2)

        return punto1, punto2

    # Crear la animación
    ani = animation.FuncAnimation(fig, animate, frames=max(len(caminos1[0]), len(caminos2[0])), init_func=init, blit=True, interval=500)
    plt.legend()
    plt.show()

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
        while i < min(len(caminos1[0]), len(caminos2[0])):
            # Verificar las siguientes posiciones
            siguiente_pos1 = caminos1[0][i + 1] if i + 1 < len(caminos1[0]) else None
            siguiente_pos2 = caminos2[0][i + 1] if i + 1 < len(caminos2[0]) else None

            # Verificar si hay colisión en las siguientes posiciones
            if siguiente_pos1 and siguiente_pos2 and detectar_colision(siguiente_pos1, siguiente_pos2):
                print(f"Colisión detectada en el paso {i + 1}!")

                # Recalcular la ruta de ambos montacargas para evitar la colisión
                caminos1_nuevo, costo1_nuevo, _ = recalcular_ruta(tablero, objetivos1, montacargas_inicio=(5, 0), obstaculo_pos=siguiente_pos2)
                caminos2_nuevo, costo2_nuevo, _ = recalcular_ruta(tablero, objetivos2, montacargas_inicio=(6, 0), obstaculo_pos=siguiente_pos1)

                # Comparar los costos y elegir el montacargas que cambiará su ruta
                if costo1_nuevo < costo2_nuevo:
                    caminos1, costo1 = caminos1_nuevo, costo1_nuevo
                    print(f"Montacargas 1 recalcula su ruta, nueva posición: {caminos1[0][i + 1]}")
                else:
                    caminos2, costo2 = caminos2_nuevo, costo2_nuevo
                    print(f"Montacargas 2 recalcula su ruta, nueva posición: {caminos2[0][i + 1]}")

            # Mostrar las posiciones de los montacargas
            print(f"Paso {i + 1} de ambos montacargas:")
            print(f"Montacargas 1 está en: {caminos1[0][i]}")
            print(f"Montacargas 2 está en: {caminos2[0][i]}")

            i += 1

        # Guardar los caminos para la animación
        animar_caminos(caminos1, caminos2, tablero)

menu()