import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def generar_mapa_calor(nuevo_orden):
    # Definir el tamaño de la grilla
    filas = 11
    columnas = 13
    
    # Crear una matriz para representar la grilla
    grilla = np.zeros((filas, columnas), dtype=int)
    
    # Asignar los productos del 1 al 48 según el nuevo orden ingresado
    ubicaciones_productos = {}
    indices = [(1,2), (1,3), (1,6), (1,7), (1,10), (1,11),
               (2,2), (2,3), (2,6), (2,7), (2,10), (2,11),
               (3,2), (3,3), (3,6), (3,7), (3,10), (3,11),
               (4,2), (4,3), (4,6), (4,7), (4,10), (4,11),
               (6,2), (6,3), (6,6), (6,7), (6,10), (6,11),
               (7,2), (7,3), (7,6), (7,7), (7,10), (7,11),
               (8,2), (8,3), (8,6), (8,7), (8,10), (8,11),
               (9,2), (9,3), (9,6), (9,7), (9,10), (9,11)]
    
    for i, pos in enumerate(indices):
        ubicaciones_productos[pos] = nuevo_orden[i]
    
    # Cargar el archivo CSV y contar la frecuencia de cada producto
    df = pd.read_csv("ordenes.csv", header=None)
    productos_lista = df.values.flatten()
    productos_lista = productos_lista[~pd.isna(productos_lista)]  # Eliminar NaN
    frecuencia_productos = {int(p): np.sum(productos_lista == int(p)) for p in np.unique(productos_lista)}
    
    # Crear una matriz de calor en la grilla
    heatmap = np.zeros((filas, columnas))
    for (i, j), producto in ubicaciones_productos.items():
        heatmap[i, j] = frecuencia_productos.get(producto, 0)
    
    # Crear la figura y el eje
    fig, ax = plt.subplots()
    
    # Dibujar el mapa de calor
    cmap = plt.cm.Reds
    ax.imshow(heatmap, cmap=cmap, origin='upper')
    
    # Dibujar las líneas de la grilla
    for i in range(filas + 1):
        ax.axhline(i - 0.5, color='black', lw=2)
    for j in range(columnas + 1):
        ax.axvline(j - 0.5, color='black', lw=2)
    
    # Mostrar los números de los productos en la grilla
    for (i, j), producto in ubicaciones_productos.items():
        ax.text(j, i, str(producto), ha='center', va='center', fontsize=10, color='blue')
    
    # Resaltar la casilla de carga (5, 0)
    ax.add_patch(plt.Rectangle((-0.5, 4.5), 1, 1, color='yellow', alpha=0.5))
    ax.text(0, 5, "C", ha='center', va='center', fontsize=12, color='black', weight='bold')
    
    # Configurar los límites y ocultar ejes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.5, columnas - 0.5)
    ax.set_ylim(filas - 0.5, -0.5)
    
    # Mostrar el gráfico
    plt.title("Mapa de Calor de Productos Más Solicitados")
    plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, label='Frecuencia de Compra')
    plt.show()

# Ejemplo de uso con un nuevo orden de productos
generar_mapa_calor(list(range(1, 49)))