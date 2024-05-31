import csv
import random
import tkinter as tk
from tkinter import ttk

# Cargar los datos de los genes desde un archivo CSV
def load_genes_from_csv(file_path):
    genes = []
    # Abre el archivo CSV en modo de lectura
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        # Itera sobre cada fila en el archivo CSV
        for row in csv_reader:
            # Convierte el precio de cadena a entero
            row['price'] = int(row['price'])
            # Convierte el consumo de energía de cadena a entero, si existe; de lo contrario, establece 0
            row['power_consumption'] = int(row['power_consumption']) if row['power_consumption'] else 0
            # Si hay datos de compatibilidad, divídelos en una lista; de lo contrario, usa una lista vacía
            if 'compatible' in row and row['compatible']:
                row['compatible'] = row['compatible'].split(';')
            else:
                row['compatible'] = []
            # Añade el gen (componente) a la lista de genes
            genes.append(row)
    return genes

# Carga todos los genes posibles desde el archivo 'components.csv'
all_possible_genes = load_genes_from_csv('components.csv')

# Definición de la clase Chromosome
class Chromosome:
    def __init__(self, genes):
        self.genes = genes  # Los genes representan los componentes seleccionados
        self.fitness = 0  # La aptitud inicial es 0
        self.total_power_consumption = 0  # Consumo total de energía inicial

    # Calcula la aptitud del cromosoma
    def calculate_fitness(self):
        # Calcula la aptitud sumando los precios de los genes (componentes)
        self.fitness = sum([gene['price'] for gene in self.genes])
        # Calcula el consumo total de energía
        self.total_power_consumption = sum([gene['power_consumption'] for gene in self.genes])

    # Realiza una mutación en el cromosoma
    def mutate(self):
        # Tasa de mutación
        mutation_rate = 0  # Porcentaje ajustable para la probabilidad de mutación
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

    # Inicializa la población
    def initialize_population(self):
        initial_population = []
        robust_processors = ['i7-10700K', 'i9-10900K', 'i7-11700K', 'i9-11900K', 'Ryzen 7 5800X', 'Ryzen 9 5900X', 'Ryzen 9 5950X']  # Define modelos de procesadores robustos

        # Crea la población inicial
        for _ in range(self.population_size):
            selected_genes = []
            processor_selected = False
            robust_processor_selected = False  # Indicador para procesador robusto

            # Selecciona componentes aleatoriamente
            for component_type in ['Procesador', 'Motherboard', 'GPU', 'RAM', 'Fuente de Poder']:
                if component_type == 'Procesador' and self.processor_preference != 'Cualquiera':
                    # Filtra opciones de procesador según la preferencia del usuario
                    component_options = [gene for gene in all_possible_genes if
                                         gene['component'] == component_type and gene['brand'] == self.processor_preference]
                elif component_type == 'GPU' and self.gpu_preference != 'Cualquiera':
                    # Filtra opciones de GPU según la preferencia del usuario
                    component_options = [gene for gene in all_possible_genes if
                                         gene['component'] == component_type and gene['brand'] == self.gpu_preference]
                elif component_type == 'Motherboard' and processor_selected:
                    # Filtra opciones de motherboard compatibles con el procesador seleccionado
                    processor_brand = next((gene['brand'] for gene in selected_genes if gene['component'] == 'Procesador'), None)
                    component_options = [gene for gene in all_possible_genes if
                                         gene['component'] == component_type and processor_brand in gene['compatible']]
                else:
                    # Selecciona componentes sin filtrado adicional
                    component_options = [gene for gene in all_possible_genes if gene['component'] == component_type]

                if component_options:
                    # Selecciona un componente aleatorio de las opciones disponibles
                    selected_gene = random.choice(component_options)
                    selected_genes.append(selected_gene)

                    if component_type == 'Procesador':
                        processor_selected = True
                        # Verifica si se seleccionó un procesador robusto
                        if selected_gene['model'] in robust_processors:
                            robust_processor_selected = True

            if robust_processor_selected:
                # Asigna implícitamente una GPU compatible con el procesador robusto
                compatible_gpus = [gene for gene in all_possible_genes if gene['component'] == 'GPU']
                if compatible_gpus:
                    selected_genes.append(random.choice(compatible_gpus))

            # Crea un cromosoma con los genes seleccionados
            chromosome = Chromosome(selected_genes)
            chromosome.calculate_fitness()
            initial_population.append(chromosome)

        return initial_population

    # Selecciona a los padres para la reproducción
    def select_parents(self):
        # Ordena la población por aptitud y selecciona los dos mejores
        self.population.sort(key=lambda x: x.fitness)
        return self.population[:2]

    # Realiza el cruce entre dos padres para crear un hijo
    def crossover(self, parent1, parent2):
        child_genes = []
        for i in range(len(parent1.genes)):
            # Selecciona genes aleatoriamente de cada padre
            if random.random() > 0.5:
                child_genes.append(parent1.genes[i])
            else:
                child_genes.append(parent2.genes[i])
        child = Chromosome(child_genes)
        child.calculate_fitness()
        return child

    # Ejecuta el algoritmo genético a través de las generaciones
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
        # Ordena la población final por aptitud
        self.population.sort(key=lambda x: x.fitness)
        # Selecciona el mejor cromosoma dentro del presupuesto
        best_chromosome = min(self.population, key=lambda x: x.fitness if x.fitness <= self.budget else float('inf'))
        return best_chromosome

# Función para ejecutar el algoritmo genético y mostrar resultados
def run_genetic_algorithm():
    # Obtiene las preferencias y presupuesto del usuario
    processor_preference = processor_var.get()
    gpu_preference = gpu_var.get()
    budget = int(budget_entry.get())
    # Inicializa y ejecuta el algoritmo genético
    ga = GeneticAlgorithm(population_size=10, generations=20, processor_preference=processor_preference, gpu_preference=gpu_preference, budget=budget)
    best_chromosome = ga.run()
    # Muestra la mejor combinación de componentes encontrada
    result_text.set("Mejor combinación:\n" + "\n".join([f"{gene['component']}: {gene['brand']} {gene['model']}" for gene in best_chromosome.genes]))

# Crear la interfaz gráfica de usuario
root = tk.Tk()
root.title("Selección de Componentes de PC")

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
    rb = ttk.Radiobutton(frame, text=text, variable=processor_var, value=value)
    rb.grid(column=1, row=processors.index((text, value)), sticky=tk.W)

# Configurar las opciones de preferencia de GPU
gpu_label = ttk.Label(frame, text="Preferencia de GPU:")
gpu_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

gpus = [("Cualquiera", "Cualquiera"), ("NVIDIA", "NVIDIA"), ("AMD", "AMD")]
for text, value in gpus:
    rb = ttk.Radiobutton(frame, text=text, variable=gpu_var, value=value)
    rb.grid(column=1, row=gpus.index((text, value)) + 3, sticky=tk.W)

# Configurar el presupuesto
budget_label = ttk.Label(frame, text="Presupuesto (MXN):")
budget_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

budget_entry = ttk.Entry(frame)
budget_entry.grid(column=1, row=6, padx=5, pady=5)

# Botón para ejecutar el algoritmo
run_button = ttk.Button(frame, text="Ejecutar", command=run_genetic_algorithm)
run_button.grid(column=0, row=7, columnspan=2, padx=5, pady=5)

# Mostrar el resultado
result_text = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result_text, relief=tk.SUNKEN)
result_label.grid(column=0, row=8, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

# Ejecutar la interfaz gráfica
root.mainloop()
