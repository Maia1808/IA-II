import numpy as np
import random
import math
from queue import PriorityQueue


class MatrizAlmacen:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = np.zeros((filas, columnas), dtype=int)  # matriz 0s

    def agregar_estante(self, fila_inicio, columna_inicio, numero_estante):
        for i in range(4):
            for j in range(2):
                self.matriz[fila_inicio + i, columna_inicio + j] = numero_estante
                numero_estante += 1

    def mostrar_matriz(self):
        for fila in self.matriz:
            print(" ".join(f"{x:2d}" if x != 0 else " 0" for x in fila))

    def obtener_posicion_adjacente(self, numero_producto):
        movimientos = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
        ]
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.matriz[i, j] == numero_producto:
                    for mov in movimientos:
                        vecino = (i + mov[0], j + mov[1])
                        if (
                            0 <= vecino[0] < self.filas
                            and 0 <= vecino[1] < self.columnas
                            and self.matriz[vecino] == 0
                        ):
                            return vecino
        return None


def a_star(matriz, inicio, fin):
    filas, columnas = matriz.shape
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    open_set = PriorityQueue()
    open_set.put((0, inicio))
    costos = {inicio: 0}

    while not open_set.empty():
        _, actual = open_set.get()
        if actual == fin:
            return costos[actual]

        for mov in movimientos:
            vecino = (actual[0] + mov[0], actual[1] + mov[1])
            if (
                0 <= vecino[0] < filas
                and 0 <= vecino[1] < columnas
                and matriz[vecino] == 0
            ):
                nuevo_costo = costos[actual] + 1
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    prioridad = (
                        nuevo_costo + abs(vecino[0] - fin[0]) + abs(vecino[1] - fin[1])
                    )
                    open_set.put((prioridad, vecino))

    return float("inf")


class TempleSimulado:
    def __init__(
        self, matriz_almacen, productos, temperatura_inicial=1000, enfriamiento=0.95
    ):
        self.matriz_almacen = matriz_almacen
        self.productos = productos
        self.temperatura = temperatura_inicial
        self.enfriamiento = enfriamiento

    def costo_ruta(self, ruta):
        costo = 0
        pos_actual = (5, 0)
        for producto in ruta:
            pos_producto = self.matriz_almacen.obtener_posicion_adjacente(producto)
            if pos_producto is None:
                raise ValueError(
                    f"No se encontró celda adyacente libre para el producto {producto}."
                )
            costo += a_star(self.matriz_almacen.matriz, pos_actual, pos_producto)
            pos_actual = pos_producto
        return costo

    def generar_vecino(self, ruta):
        vecino = ruta.copy()
        i, j = random.sample(range(len(vecino)), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return vecino

    def temple_simulado(self):
        ruta_actual = self.productos.copy()
        random.shuffle(ruta_actual)
        costo_actual = self.costo_ruta(ruta_actual)

        mejor_ruta = ruta_actual.copy()
        mejor_costo = costo_actual

        while self.temperatura > 1:
            ruta_vecina = self.generar_vecino(ruta_actual)
            costo_vecino = self.costo_ruta(ruta_vecina)

            if costo_vecino < costo_actual or random.random() < math.exp(
                (costo_actual - costo_vecino) / self.temperatura
            ):
                ruta_actual = ruta_vecina
                costo_actual = costo_vecino

                if costo_actual < mejor_costo:
                    mejor_ruta = ruta_actual.copy()
                    mejor_costo = costo_actual

            self.temperatura *= self.enfriamiento

        if mejor_costo == float("inf"):
            raise ValueError(
                "No se encontró una ruta válida para la configuración dada."
            )

        return mejor_ruta, mejor_costo


almacen = MatrizAlmacen(11, 13)

posiciones_estantes = [
    (1, 2),
    (1, 6),
    (1, 10),
    (6, 2),
    (6, 6),
    (6, 10),
]

# Asignar productos a los estantes (del 1 al 48)
numero_producto = 1
for fila_inicio, columna_inicio in posiciones_estantes:
    almacen.agregar_estante(fila_inicio, columna_inicio, numero_producto)
    numero_producto += 8

# Mostrar la matriz con los productos
print("Matriz del almacén con productos:")
almacen.mostrar_matriz()

# Lista de productos a buscar
productos = [22, 2, 12]

# Ejecutar el temple simulado
temple = TempleSimulado(almacen, productos)
mejor_ruta, mejor_costo = temple.temple_simulado()

print(f"\nMejor ruta encontrada: {mejor_ruta}")
print(f"Costo de la mejor ruta: {mejor_costo}")
