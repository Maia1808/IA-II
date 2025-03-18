import random
import pandas as pd
import numpy as np

class AlgoritmoGenetico:
    def __init__(self, num_individuals=10, num_genes=48, csv='ordenes.csv'):
        self.population = []
        self.num_individuals = num_individuals
        self.num_genes = num_genes
        self.csv = csv

    def initialize_population(self):
        products = list(range(1, self.num_genes + 1))  # Productos identificados del 1 al N
        
        for _ in range(self.num_individuals):
            individual = random.sample(products, self.num_genes)  # Genera una permutación aleatoria
            self.population.append(individual)

        return self.population

    def evaluate_population(self):
        orders = pd.read_csv(self.csv, header=None)
        
        fitness_scores = []
        
        for individual in self.population:
            total_cost = 0
            
            for _, row in orders.iterrows(): # HAY QUE ELEGIR UN CIERTO N DE PEDIDOS ACA
                pedido = row.dropna().astype(int).tolist()
                total_cost += temple_simulado(individual, pedido) # IMPLEMENTAR TEMPLE SIMULADO 
            
            fitness_scores.append(total_cost)

        fitness_scores_norm = [1 - (score / sum(fitness_scores)) for score in fitness_scores]

        return fitness_scores_norm

    def new_population(self, fitness_scores_norm):
        new_population = []  # Lista para almacenar los nuevos individuos

        for _ in range(5):  # 5 pares de padres -> 10 hijos
            parent1, parent2 = np.random.choice(
                self.population, size=2, replace=False, p=fitness_scores_norm
            )

            size = len(parent1)
            start, end = size // 3, 2 * size // 3  # Definir el tercio central
            child1, child2 = [-1] * size, [-1] * size

            # Copiar los elementos del tercio central al hijo correspondiente
            child1[start:end] = parent1[start:end]
            child2[start:end] = parent2[start:end]

            # Función para rellenar los espacios vacíos respetando el orden del otro padre
            def fill_child(child, parent_source):
                insert_idx = 0  # Empezamos desde el inicio
                for gene in parent_source:
                    if gene not in child:
                        while child[insert_idx] != -1:  # Saltamos posiciones ya ocupadas
                            insert_idx += 1
                        child[insert_idx] = gene

            # Llenamos los hijos con los genes del otro padre
            fill_child(child1, parent2)
            fill_child(child2, parent1)

            # Aplicamos mutación
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)

            # Agregar hijos a la nueva población
            new_population.append(child1)
            new_population.append(child2)

        self.population = new_population  # Retorna los 10 hijos generados
    
    def mutate(self, individual, mutation_rate=0.1):
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
    for _ in range(100):
        fitness_scores = ag.evaluate_population()
        ag.new_population(fitness_scores)
    ag.show_population()
