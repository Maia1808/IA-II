import heapq
import numpy as np
import matplotlib.pyplot as plt

class AEstrella:
    def __init__(self, tablero, inicio=(5, 0)):
        self.tablero = tablero
        self.inicio = inicio
        self.direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimientos: derecha, izquierda, abajo, arriba

    def heuristica(self, actual, objetivo):
        return abs(actual[0] - objetivo[0]) + abs(actual[1] - objetivo[1])  # Distancia de Manhattan

    def obtener_vecinos(self, nodo):
        vecinos = []
        for d in self.direcciones:
            nuevo = (nodo[0] + d[0], nodo[1] + d[1])
            if 0 <= nuevo[0] < self.tablero.shape[0] and 0 <= nuevo[1] < self.tablero.shape[1]:
                if self.tablero[nuevo] == 0:  # Solo se puede mover por celdas vacías
                    vecinos.append(nuevo)
        return vecinos

    def encontrar_casilla_adyacente(self, objetivo):
        fila, columna = objetivo
        if self.tablero[fila, columna] != 0:  # Si es una estantería, buscar casilla adyacente
            if columna - 1 >= 0 and self.tablero[fila, columna - 1] == 0:
                return (fila, columna - 1)  # Izquierda
            elif columna + 1 < self.tablero.shape[1] and self.tablero[fila, columna + 1] == 0:
                return (fila, columna + 1)  # Derecha
        return None

    def calcular_ruta_con_costos(self, inicio, objetivo):
        """Método para calcular la ruta del montacargas y su costo, basándose en A*."""
        frontera = []
        heapq.heappush(frontera, (0, inicio))
        visitados = {inicio: None}
        costos = {inicio: 0}

        while frontera:
            _, actual = heapq.heappop(frontera)
            
            if actual == objetivo:
                return self.reconstruir_camino(visitados, actual), costos[actual]

            for vecino in self.obtener_vecinos(actual):
                nuevo_costo = costos[actual] + 1  # Costo unitario
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    prioridad = nuevo_costo + self.heuristica(vecino, objetivo)
                    heapq.heappush(frontera, (prioridad, vecino))
                    visitados[vecino] = actual
        
        return None, float('inf')  # No hay camino

    def reconstruir_camino(self, visitados, actual):
        camino = []
        while actual is not None:
            camino.append(actual)
            actual = visitados[actual]
        camino.reverse()
        return camino
    
    def detectar_colision(self, camino_1, camino_2):
        """Detectar si hay colisión entre las rutas de los montacargas"""
        for paso_1 in camino_1:
            for paso_2 in camino_2:
                if paso_1 == paso_2:
                    return True
        return False
    
    def graficar_camino(self, caminos, objetivos_numeros):
        color_unico = 'green'  # Definir un color único para todos los caminos
        tablero_grafico = np.copy(self.tablero)
        fig, ax = plt.subplots()

        # Unir todos los caminos en uno solo
        todos_los_pasos = []
        for camino in caminos:
            todos_los_pasos.extend(camino)

        # Dibujar todos los pasos del camino con el mismo color
        for x, y in todos_los_pasos:
            ax.add_patch(plt.Rectangle((y, x), 1, 1, color=color_unico, alpha=0.5, edgecolor='black'))

        # Dibujar la cuadrícula
        for i in range(tablero_grafico.shape[0] + 1):
            ax.axhline(i, color='black', lw=1)
        for j in range(tablero_grafico.shape[1] + 1):
            ax.axvline(j, color='black', lw=1)

        # Numerar las casillas con obstáculos
        for i in range(tablero_grafico.shape[0]):
            for j in range(tablero_grafico.shape[1]):
                if self.tablero[i, j] != 0:
                    ax.text(j + 0.5, i + 0.5, str(self.tablero[i, j]), ha='center', va='center', fontsize=10, color='black')

        # Título con los objetivos
        titulo = "Camino - " + ", ".join(map(str, objetivos_numeros))
        ax.set_xlim(0, tablero_grafico.shape[1])
        ax.set_ylim(0, tablero_grafico.shape[0])
        plt.gca().invert_yaxis()
        plt.title(titulo)
        plt.show()
