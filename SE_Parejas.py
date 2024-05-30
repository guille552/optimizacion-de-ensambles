import csv
import random
import tkinter as tk
from tkinter import ttk

# Cargar los datos de los genes desde un archivo CSV
def load_genes_from_csv(file_path):
    genes = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row['price'] = int(row['price'])  # Convertir el precio a entero
            row['power_consumption'] = int(row['power_consumption']) if row['power_consumption'] else 0
            if 'compatible' in row and row['compatible']:
                row['compatible'] = row['compatible'].split(';')  # Convertir la compatibilidad a una lista
            else:
                row['compatible'] = []
            genes.append(row)
    return genes

all_possible_genes = load_genes_from_csv('components.csv')

# Definición de la clase Chromosome
class Chromosome:
    def __init__(self, genes):
        self.genes = genes  # Los genes representan los componentes seleccionados
        self.fitness = 0  # La aptitud inicial es 0
        self.total_power_consumption = 0  # Consumo total de energía inicial

    def calculate_fitness(self):
        # Calcula la aptitud sumando los precios de los genes (componentes)
        self.fitness = sum([gene['price'] for gene in self.genes])
        # Calcula el consumo total de energía
        self.total_power_consumption = sum([gene['power_consumption'] for gene in self.genes])

    def mutate(self):
        # Tasa de mutación
        mutation_rate = 0
        # Si ocurre una mutación, se reemplaza un gen por otro aleatorio
        if random.random() < mutation_rate:
            index = random.randint(0, len(self.genes) - 1)
            self.genes[index] = random.choice(all_possible_genes)

# Definición de la clase GeneticAlgorithm
class GeneticAlgorithm:
    def __init__(self, population_size, generations, processor_preference, gpu_preference, budget):
        self.population_size = population_size  # Tamaño de la población
        self.generations = generations  # Número de generaciones
        self.processor_preference = processor_preference  # Preferencia de procesador
        self.gpu_preference = gpu_preference  # Preferencia de GPU
        self.budget = budget  # Presupuesto disponible
        self.population = self.initialize_population()  # Población inicial

    def initialize_population(self):
        initial_population = []
        for _ in range(self.population_size):
            selected_genes = []
            budget_remaining = self.budget
            processor_selected = False
            motherboard_selected = False
            for component_type in ['Procesador', 'Motherboard', 'GPU', 'RAM', 'Fuente de Poder']:
                # Selección de componentes según las preferencias
                if component_type == 'Procesador' and self.processor_preference != 'Cualquiera':
                    component_options = [gene for gene in all_possible_genes if gene['component'] == component_type and gene['brand'] == self.processor_preference]
                elif component_type == 'GPU' and self.gpu_preference != 'Cualquiera':
                    component_options = [gene for gene in all_possible_genes if gene['component'] == component_type and gene['brand'] == self.gpu_preference]
                elif component_type == 'Motherboard' and processor_selected:
                    processor_brand = next((gene['brand'] for gene in selected_genes if gene['component'] == 'Procesador'), None)
                    component_options = [gene for gene in all_possible_genes if gene['component'] == component_type and processor_brand in gene['compatible']]
                else:
                    component_options = [gene for gene in all_possible_genes if gene['component'] == component_type]
                
                # Filtrado de componentes asequibles dentro del presupuesto restante
                affordable_options = [gene for gene in component_options if gene['price'] <= budget_remaining]
                if affordable_options:
                    selected_gene = random.choice(affordable_options)
                    selected_genes.append(selected_gene)
                    budget_remaining -= selected_gene['price']
                    
                    if component_type == 'Procesador':
                        processor_selected = True
                    elif component_type == 'Motherboard':
                        motherboard_selected = True
                else:
                    selected_genes.append(random.choice(component_options))
            chromosome = Chromosome(selected_genes)
            chromosome.calculate_fitness()
            initial_population.append(chromosome)
        return initial_population

    def select_parents(self):
        # Ordena la población por aptitud y selecciona los dos mejores para reproducción
        self.population.sort(key=lambda x: x.fitness)
        return self.population[:2]

    def crossover(self, parent1, parent2):
        # Cruce de genes de los padres para crear un hijo
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
        # Ejecuta el algoritmo genético a través de las generaciones
        for _ in range(self.generations):
            new_population = []
            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents()
                child = self.crossover(parent1, parent2)
                child.mutate()
                child.calculate_fitness()
                new_population.append(child)
            self.population = new_population
        self.population.sort(key=lambda x: x.fitness)
        return self.population[0]

# Función para ejecutar el algoritmo genético y mostrar resultados
def run_genetic_algorithm():
    processor_preference = processor_var.get()
    gpu_preference = gpu_var.get()
    budget = int(budget_entry.get())
    ga = GeneticAlgorithm(population_size=10, generations=20, processor_preference=processor_preference, gpu_preference=gpu_preference, budget=budget)
    best_chromosome = ga.run()
    result_text.set("Mejor combinación:\n" + "\n".join([f"{gene['component']}: {gene['brand']} {gene['model']} - Precio: {gene['price']} - Consumo de Energía: {gene['power_consumption']}W" for gene in best_chromosome.genes]))

# Crear la interfaz gráfica de usuario
root = tk.Tk()
root.title("Selección de Componentes de PC con Algoritmo Genético")

# Estilo
style = ttk.Style(root)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))

# Variables para las opciones seleccionables
processor_var = tk.StringVar(value="Cualquiera")
gpu_var = tk.StringVar(value="Cualquiera")

# Configurar las opciones de preferencia de procesador
frame = ttk.Frame(root, padding="10 10 10 10")
frame.pack(fill=tk.BOTH, expand=True)

processor_label = ttk.Label(frame, text="Preferencia de Procesador:")
processor_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

processors = [("Cualquiera", "Cualquiera"), ("Intel", "Intel"), ("AMD", "AMD")]
for text, value in processors:
    ttk.Radiobutton(frame, text=text, variable=processor_var, value=value).grid(column=1, row=processors.index((text, value)), sticky=tk.W, padx=5, pady=2)

# Configurar las opciones de preferencia de GPU
gpu_label = ttk.Label(frame, text="Preferencia de GPU:")
gpu_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

gpus = [("Cualquiera", "Cualquiera"), ("NVIDIA", "NVIDIA"), ("AMD", "AMD")]
for text, value in gpus:
    ttk.Radiobutton(frame, text=text, variable=gpu_var, value=value).grid(column=1, row=gpus.index((text, value)) + 3, sticky=tk.W, padx=5, pady=2)

# Configurar la entrada del presupuesto
budget_label = ttk.Label(frame, text="Presupuesto (en USD):")
budget_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
budget_entry = ttk.Entry(frame)
budget_entry.grid(column=1, row=6, sticky=tk.E, padx=5, pady=5)

# Configurar el botón para ejecutar el algoritmo genético
run_button = ttk.Button(frame, text="Ejecutar", command=run_genetic_algorithm)
run_button.grid(column=0, row=7, columnspan=2, pady=10)

# Configurar el campo de texto para mostrar los resultados
result_text = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result_text, relief="sunken", padding="5 5 5 5")
result_label.grid(column=0, row=8, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=10)

root.mainloop()
