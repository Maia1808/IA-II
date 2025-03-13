import matplotlib.pyplot as plt
import numpy as np

# Definir el tamaño de la grilla
filas = 11
columnas = 13

# Crear una matriz para representar la grilla
grilla = np.zeros((filas, columnas), dtype=int)

# Asignar los productos del 1 al 24
grilla[1, 2] = 1
grilla[1, 3] = 2
grilla[1, 6] = 9
grilla[1, 7] = 10
grilla[1, 10] = 17
grilla[1, 11] = 18

grilla[2, 2] = 3
grilla[2, 3] = 4
grilla[2, 6] = 11
grilla[2, 7] = 12
grilla[2, 10] = 19
grilla[2, 11] = 20

grilla[3, 2] = 5
grilla[3, 3] = 6
grilla[3, 6] = 13
grilla[3, 7] = 14
grilla[3, 10] = 21
grilla[3, 11] = 22

grilla[4, 2] = 7
grilla[4, 3] = 8
grilla[4, 6] = 15
grilla[4, 7] = 16
grilla[4, 10] = 23
grilla[4, 11] = 24

# Asignar los productos del 25 al 48
grilla[6, 2] = 25
grilla[6, 3] = 26
grilla[6, 6] = 33
grilla[6, 7] = 34
grilla[6, 10] = 41
grilla[6, 11] = 42

grilla[7, 2] = 27
grilla[7, 3] = 28
grilla[7, 6] = 35
grilla[7, 7] = 36
grilla[7, 10] = 43
grilla[7, 11] = 44

grilla[8, 2] = 29
grilla[8, 3] = 30
grilla[8, 6] = 37
grilla[8, 7] = 38
grilla[8, 10] = 45
grilla[8, 11] = 46

grilla[9, 2] = 31
grilla[9, 3] = 32
grilla[9, 6] = 39
grilla[9, 7] = 40
grilla[9, 10] = 47
grilla[9, 11] = 48

# Crear la figura y el eje
fig, ax = plt.subplots()

# Dibujar la grilla
for i in range(filas + 1):
    ax.axhline(i, color='black', lw=2)

for j in range(columnas + 1):
    ax.axvline(j, color='black', lw=2)

# Mostrar los números en las casillas
for i in range(filas):
    for j in range(columnas):
        if grilla[i, j] != 0:
            ax.text(j + 0.5, i + 0.5, str(grilla[i, j]), 
                    ha='center', va='center', fontsize=10, color='blue')

# Resaltar la casilla de carga (5, 0) en amarillo con una "C"
ax.add_patch(plt.Rectangle((0, 5), 1, 1, color='yellow', alpha=0.5))  # Fondo amarillo
ax.text(0.5, 5.5, "C", ha='center', va='center', fontsize=12, color='black', weight='bold')

# Configurar los límites del gráfico
ax.set_xlim(0, columnas)
ax.set_ylim(0, filas)

# Ocultar los ejes
ax.set_xticks([])
ax.set_yticks([])

# Invertir el eje y para que la fila 0 esté arriba
plt.gca().invert_yaxis()

# Mostrar la grilla
plt.title("Supermercado - Grilla de Estanterías y Pasillos")
plt.show()