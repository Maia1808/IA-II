import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from TP1IA import TempleSimulado, MatrizAlmacen

class AlgoritmoGenetico:
    def __init__(self, num_individuals=10, num_genes=48, csv='ordenes.csv'):
        self.population = []
        self.num_individuals = num_individuals
        self.num_genes = num_genes
        self.csv = csv
        self.orders = pd.read_csv(self.csv, header=None)

    def initialize_population(self):
        products = list(range(1, self.num_genes + 1))  # Productos identificados del 1 al N
        
        for _ in range(self.num_individuals):
            individual = random.sample(products, self.num_genes)  # Genera una permutación aleatoria
            self.population.append(individual)

        return self.population

    def evaluate_individual(self, almacen, number_rows):
        
        # Seleccionar siempre las primeras n órdenes
        orders_sample = self.orders.head(number_rows)
            
        total_cost = 0
        
        for _, row in orders_sample.iterrows(): 
            pedido = row.dropna().astype(int).tolist()
            temple = TempleSimulado(almacen, pedido)
            _, costo = temple.temple_simulado() # TEMPLE SIMULADO 
            total_cost += costo

        return total_cost # Devuelve la lista de scores normalizados probabilisticamente

    def new_population(self, fitness_scores_norm):
        new_population = []

        # Obtener el índice del mejor padre (mayor fitness)
        best_parent_idx = np.argmax(fitness_scores_norm)
        best_parent = self.population[best_parent_idx]

        # Agregar el mejor individuo directamente a la nueva generación (elitismo)
        new_population.append(best_parent)

        # Obtener los índices de los 5 mejores padres restantes (sin contar el mejor)
        top_parents_indices = np.argsort(fitness_scores_norm)[-6:]  # Tomamos 6 y excluimos el mejor
        top_parents_indices = top_parents_indices[top_parents_indices != best_parent_idx]  # Excluir el mejor

        for _ in range(5):  # 5 pares de padres -> 10 hijos en total
            idx1, idx2 = np.random.choice(top_parents_indices, size=2, replace=False)

            parent1 = self.population[idx1]
            parent2 = self.population[idx2]

            # Aplicar PMX
            child1, child2 = self.pmx_crossover(parent1, parent2)

            # Aplicar mutación
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)

            new_population.append(child1)
            new_population.append(child2)

        # Asegurar que la población sigue siendo de 10 individuos
        self.population = new_population[:self.num_individuals]

    def pmx_crossover(self, parent1, parent2):
        """Implementación del cruce PMX (Partially Mapped Crossover)."""
        size = len(parent1)
        start, end = sorted(np.random.choice(range(size), size=2, replace=False))  # Selección aleatoria de puntos de cruce

        # Inicializar hijos con -1
        child1, child2 = [-1] * size, [-1] * size

        # Copiar segmento central de los padres a los hijos
        child1[start:end] = parent1[start:end]
        child2[start:end] = parent2[start:end]

        # Crear mapeo de genes entre padres
        mapping1 = {parent1[i]: parent2[i] for i in range(start, end)}
        mapping2 = {parent2[i]: parent1[i] for i in range(start, end)}

        # Función para completar los hijos respetando el mapeo
        def fill_pmx(child, parent, mapping):
            for i in range(size):
                if child[i] == -1:  # Si el gen aún no está asignado
                    candidate = parent[i]
                    while candidate in mapping:  # Resolver conflictos por mapeo
                        candidate = mapping[candidate]
                    child[i] = candidate

        # Llenar los hijos con los genes restantes usando el mapeo
        fill_pmx(child1, parent2, mapping1)
        fill_pmx(child2, parent1, mapping2)

        return child1, child2
    
    def mutate(self, individual, mutation_rate=0.15):
        """ Aplica mutación con cierta probabilidad """
        if random.random() < mutation_rate:  # Se ejecuta con probabilidad mutation_rate
            size = len(individual)
            idx1, idx2 = random.sample(range(size), 2)  # Elegir 2 posiciones aleatorias
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]  # Intercambio
        
        return individual
    
    def show_population(self):
        """Muestra la población actual de individuos en la consola."""
        print("\n=== Población Actual ===")
        for idx, individual in enumerate(self.population, start=1):
            print(f"Individuo {idx}: {individual}")
        print("========================\n")


if __name__ == "__main__":
    ag = AlgoritmoGenetico()
    ag.initialize_population()

    # Crear almacén
    almacen = MatrizAlmacen(11, 13)
    
    posiciones_estantes = [
        (1, 2),
        (1, 6),
        (1, 10),
        (6, 2),
        (6, 6),
        (6, 10),
    ]
    
    iteracion = 0
    promedio_costos_lista = []

    for _ in range(100):
        costos_individuos = [] 
        iteracion += 1

        for individuo in range(ag.num_individuals):
            almacen.asignar_estantes_con_vector(ag.population[individuo], posiciones_estantes)
            costo = ag.evaluate_individual(almacen, 6)
            costos_individuos.append(costo)

        print(costos_individuos)

        promedio_costos = np.mean(costos_individuos)
        promedio_costos_lista.append(promedio_costos)
        print(f"Iteración {iteracion}: Costo promedio = {promedio_costos}")

        sum_costos = sum(1 / np.array(costos_individuos))  # Sumar inversos de costos
        fitness_scores_norm = [(1/costo) / sum_costos if sum_costos > 0 else 0 for costo in costos_individuos]

        ag.new_population(fitness_scores_norm)
    
    # Encontrar el individuo con el menor costo
    min_cost_idx = np.argmin(costos_individuos)  # Índice del individuo con menor costo
    best_individual = ag.population[min_cost_idx]  # Obtener el mejor individuo
    best_cost = costos_individuos[min_cost_idx]  # Obtener su costo

    # Mostrar el mejor individuo y su costo
    print("\nMejor individuo encontrado:")
    print("Individuo:", best_individual)
    print("Costo asociado:", best_cost)

    # **Graficar la evolución del costo promedio**
    plt.plot(range(1, iteracion + 1), promedio_costos_lista, marker='o', linestyle='-')
    plt.xlabel("Iteración")
    plt.ylabel("Costo promedio")
    plt.title("Evolución del costo promedio en el Algoritmo Genético")
    plt.grid()
    plt.show()



    

        