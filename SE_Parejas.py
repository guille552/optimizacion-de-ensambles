import random
import tkinter as tk
from tkinter import ttk

# Ejemplo de posibles genes (componentes)
all_possible_genes = [
    {'component': 'Procesador', 'brand': 'Intel', 'model': 'i9', 'score': 90, 'price': 500},
    {'component': 'Procesador', 'brand': 'Intel', 'model': 'i7', 'score': 85, 'price': 400},
    {'component': 'Procesador', 'brand': 'Intel', 'model': 'i5', 'score': 75, 'price': 300},
    {'component': 'Procesador', 'brand': 'AMD', 'model': 'Ryzen 9', 'score': 88, 'price': 450},
    {'component': 'Procesador', 'brand': 'AMD', 'model': 'Ryzen 7', 'score': 85, 'price': 400},
    {'component': 'Procesador', 'brand': 'AMD', 'model': 'Ryzen 5', 'score': 78, 'price': 350},
    {'component': 'GPU', 'brand': 'NVIDIA', 'model': 'RTX 3080', 'score': 95, 'price': 1000},
    {'component': 'GPU', 'brand': 'NVIDIA', 'model': 'RTX 3070', 'score': 90, 'price': 800},
    {'component': 'GPU', 'brand': 'NVIDIA', 'model': 'RTX 3060', 'score': 85, 'price': 600},
    {'component': 'GPU', 'brand': 'AMD', 'model': 'RX 6900 XT', 'score': 94, 'price': 900},
    {'component': 'GPU', 'brand': 'AMD', 'model': 'RX 6800 XT', 'score': 90, 'price': 800},
    {'component': 'GPU', 'brand': 'AMD', 'model': 'RX 6700 XT', 'score': 85, 'price': 700},
    {'component': 'RAM', 'brand': 'Corsair', 'model': '16GB', 'score': 80, 'price': 200},
    {'component': 'RAM', 'brand': 'Corsair', 'model': '32GB', 'score': 90, 'price': 350},
    {'component': 'RAM', 'brand': 'G.Skill', 'model': '16GB', 'score': 75, 'price': 150},
    {'component': 'RAM', 'brand': 'G.Skill', 'model': '32GB', 'score': 85, 'price': 300},
    {'component': 'RAM', 'brand': 'Kingston', 'model': '16GB', 'score': 78, 'price': 180},
    {'component': 'RAM', 'brand': 'Kingston', 'model': '32GB', 'score': 88, 'price': 330},
    {'component': 'Procesador', 'brand': 'Intel', 'model': 'i3', 'score': 65, 'price': 200},
    {'component': 'Procesador', 'brand': 'AMD', 'model': 'Ryzen 3', 'score': 68, 'price': 250},
    {'component': 'GPU', 'brand': 'NVIDIA', 'model': 'GTX 1660', 'score': 80, 'price': 500},
    {'component': 'GPU', 'brand': 'AMD', 'model': 'RX 5600 XT', 'score': 82, 'price': 550},
    {'component': 'RAM', 'brand': 'Crucial', 'model': '16GB', 'score': 76, 'price': 160},
    {'component': 'RAM', 'brand': 'Crucial', 'model': '32GB', 'score': 86, 'price': 310},
    # Añadir más componentes según sea necesario
]

class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

    def calculate_fitness(self):
        self.fitness = sum([gene['score'] for gene in self.genes])

    def mutate(self):
        mutation_rate = 0
        if random.random() < mutation_rate:
            index = random.randint(0, len(self.genes) - 1)
            self.genes[index] = random.choice(all_possible_genes)

class GeneticAlgorithm:
    def __init__(self, population_size, generations, processor_preference, gpu_preference, budget):
        self.population_size = population_size
        self.generations = generations
        self.processor_preference = processor_preference
        self.gpu_preference = gpu_preference
        self.budget = budget
        self.population = self.initialize_population()

    def initialize_population(self):
        initial_population = []
        for _ in range(self.population_size):
            selected_genes = []
            budget_remaining = self.budget
            for component_type in ['Procesador', 'GPU', 'RAM']:
                if component_type == 'Procesador' and self.processor_preference != 'Cualquiera':
                    component_options = [gene for gene in all_possible_genes if gene['component'] == component_type and gene['brand'] == self.processor_preference]
                elif component_type == 'GPU' and self.gpu_preference != 'Cualquiera':
                    component_options = [gene for gene in all_possible_genes if gene['component'] == component_type and gene['brand'] == self.gpu_preference]
                else:
                    component_options = [gene for gene in all_possible_genes if gene['component'] == component_type]
                
                affordable_options = [gene for gene in component_options if gene['price'] <= budget_remaining]
                if affordable_options:
                    selected_gene = random.choice(affordable_options)
                    selected_genes.append(selected_gene)
                    budget_remaining -= selected_gene['price']
                else:
                    selected_genes.append(random.choice(component_options))
            chromosome = Chromosome(selected_genes)
            chromosome.calculate_fitness()
            initial_population.append(chromosome)
        return initial_population

    def select_parents(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        return self.population[:2]

    def crossover(self, parent1, parent2):
        child_genes = []
        for i in range(len(parent1.genes)):
            if random.random() > 0.5:
                child_genes.append(parent1.genes[i])
            else:
                child_genes.append(parent2.genes[i])
        child = Chromosome(child_genes)
        child.calculate_fitness()
        return child

    def run(self):
        for _ in range(self.generations):
            new_population = []
            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents()
                child = self.crossover(parent1, parent2)
                child.mutate()
                child.calculate_fitness()
                new_population.append(child)
            self.population = new_population
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        return self.population[0]

def run_genetic_algorithm():
    processor_preference = processor_combobox.get()
    gpu_preference = gpu_combobox.get()
    budget = int(budget_entry.get())
    ga = GeneticAlgorithm(population_size=10, generations=20, processor_preference=processor_preference, gpu_preference=gpu_preference, budget=budget)
    best_chromosome = ga.run()
    result_text.set("Mejor combinación:\n" + "\n".join([f"{gene['component']}: {gene['brand']} {gene['model']} - Precio: {gene['price']} - Puntuación: {gene['score']}" for gene in best_chromosome.genes]))

# Crear la interfaz gráfica de usuario
root = tk.Tk()
root.title("Selección de Componentes de PC con Algoritmo Genético")

# Configurar las opciones de preferencia de procesador y GPU
processor_label = ttk.Label(root, text="Preferencia de Procesador:")
processor_label.pack()
processor_combobox = ttk.Combobox(root, values=["Cualquiera", "Intel", "AMD"])
processor_combobox.set("Cualquiera")
processor_combobox.pack()

gpu_label = ttk.Label(root, text="Preferencia de GPU:")
gpu_label.pack()
gpu_combobox = ttk.Combobox(root, values=["Cualquiera", "NVIDIA", "AMD"])
gpu_combobox.set("Cualquiera")
gpu_combobox.pack()

# Configurar el presupuesto
budget_label = ttk.Label(root, text="Presupuesto (en $):")
budget_label.pack()
budget_entry = ttk.Entry(root)
budget_entry.pack()

# Botón para ejecutar el algoritmo genético
run_button = ttk.Button(root, text="Generate", command=run_genetic_algorithm)
run_button.pack()

# Mostrar el resultado
result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text)
result_label.pack()

root.mainloop()
