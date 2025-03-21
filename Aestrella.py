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

    def buscar_camino(self, objetivos):
        if isinstance(objetivos, tuple):  # Si es un solo objetivo, convertirlo en lista
            objetivos = [objetivos]
        
        camino_total = []
        costo_total = 0
        actual = self.inicio
        caminos = []

        for objetivo in objetivos:
            destino = self.encontrar_casilla_adyacente(objetivo)
            if not destino:
                print(f"No se encontró una casilla accesible para el objetivo {objetivo}")
                continue
            
            camino, costo = self.algoritmo_a_estrella(actual, destino)
            if camino:
                camino = [tuple(map(int, paso)) for paso in camino]  # Convertir np.int64 a int
                caminos.append(camino)
                camino_total.extend(camino)
                costo_total += costo
                actual = destino
        
        return caminos, costo_total

    def algoritmo_a_estrella(self, inicio, objetivo):
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

    def graficar_camino(self, caminos, objetivos_numeros):
        colores = ['green', 'blue', 'red', 'purple', 'orange']  # Colores para diferenciar caminos
        tablero_grafico = np.copy(self.tablero)
        fig, ax = plt.subplots()
        
        for i, camino in enumerate(caminos):
            for x, y in camino:
                ax.add_patch(plt.Rectangle((y, x), 1, 1, color=colores[i % len(colores)], alpha=0.5, edgecolor='black'))
        
        for i in range(tablero_grafico.shape[0] + 1):
            ax.axhline(i, color='black', lw=1)
        for j in range(tablero_grafico.shape[1] + 1):
            ax.axvline(j, color='black', lw=1)
        
        for i in range(tablero_grafico.shape[0]):
            for j in range(tablero_grafico.shape[1]):
                if self.tablero[i, j] != 0:
                    ax.text(j + 0.5, i + 0.5, str(self.tablero[i, j]), ha='center', va='center', fontsize=10, color='black')
        
        titulo = "Camino - " + ", ".join(map(str, objetivos_numeros))
        ax.set_xlim(0, tablero_grafico.shape[1])
        ax.set_ylim(0, tablero_grafico.shape[0])
        plt.gca().invert_yaxis()
        plt.title(titulo)
        plt.show()
