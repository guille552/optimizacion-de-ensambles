import random
import tkinter as tk
from tkinter import ttk
from genetic_algorithm import GeneticAlgorithm  # Suponiendo que tienes una implementación de algoritmos genéticos

# Definir los parámetros de cada componente
procesadores = [
    "Intel Core i9-12900K|3.2|16/24|30|125",
    "AMD Ryzen 9 5950X|3.4|16/32|64|105",
    # Agregar más procesadores según sea necesario
]

tarjetas_graficas = [
    "NVIDIA GeForce RTX 3080|10|8704|1710|320",
    "AMD Radeon RX 6900 XT|16|5120|2250|300",
    # Agregar más tarjetas gráficas según sea necesario
]

placas_base = [
    "ASUS ROG Strix Z690-E Gaming|LGA 1700|3|128GB DDR5 6400",
    "MSI MAG B660M Bazooka|LGA 1700|2|64GB DDR4 4600",
    # Agregar más placas base según sea necesario
]

memorias_ram = [
    "Corsair Vengeance LPX DDR4 3600MHz|16|DDR4|3600|CL18",
    "G.Skill Trident Z Neo DDR4 4800MHz|32|DDR4|4800|CL19",
    # Agregar más memorias RAM según sea necesario
]

almacenamientos = [
    "Samsung 970 EVO Plus NVMe SSD|1TB|NVMe|3500/3300",
    "Seagate Barracuda HDD|4TB|SATA|190/180",
    # Agregar más almacenamientos según sea necesario
]

fuentes_alimentacion = [
    "EVGA SuperNOVA 850 G5|850|80 Plus Gold|Fully Modular",
    "Corsair RM850x|850|80 Plus Gold|Fully Modular",
    # Agregar más fuentes de alimentación según sea necesario
]

cajas = [
    "NZXT H510|ATX|Mid Tower|3x120mm Fans",
    "Fractal Design Meshify C|ATX|Mid Tower|2x120mm Fans",
    # Agregar más cajas según sea necesario
]

refrigeraciones = [
    "Noctua NH-D15|Air|140mm Fans|24.6|300",
    "Corsair H100i RGB Platinum|Liquid|240mm Radiator|37.6|240",
    # Agregar más opciones de refrigeración según sea necesario
]

# Definir clase para el algoritmo genético
class EnsamblajePCGenetico(GeneticAlgorithm):
    def __init__(self, poblacion_inicial):
        super().__init__(poblacion_inicial)

    def evaluar_fitness(self, individuo):
        # Función de evaluación de fitness (por ejemplo, rendimiento del ensamblaje)
        return random.uniform(0, 100)

    def seleccionar_padres(self, poblacion, fitness):
        # Selección de padres para cruzamiento (por ejemplo, torneo)
        return random.sample(poblacion, 2)

    def cruzar_individuos(self, padre1, padre2):
        # Cruzamiento de individuos (por ejemplo, intercambio de componentes)
        punto_corte = random.randint(1, len(padre1) - 1)
        hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
        hijo2 = padre2[:punto_corte] + padre1[punto_corte:]
        return hijo1, hijo2

    def mutar_individuo(self, individuo):
        # Mutación de individuos (por ejemplo, cambio aleatorio de componentes)
        indice_mutacion = random.randint(0, len(individuo) - 1)
        nuevo_valor = random.choice(procesadores + tarjetas_graficas + placas_base + memorias_ram + almacenamientos + fuentes_alimentacion + cajas + refrigeraciones)
        individuo_mutado = list(individuo)
        individuo_mutado[indice_mutacion] = nuevo_valor
        return ''.join(individuo_mutado)

def optimizar_ensamblaje():
    poblacion_inicial = [
        random.choice(procesadores) + "|" + random.choice(tarjetas_graficas) + "|" + random.choice(placas_base) + "|" +
        random.choice(memorias_ram) + "|" + random.choice(almacenamientos) + "|" + random.choice(fuentes_alimentacion) + "|" +
        random.choice(cajas) + "|" + random.choice(refrigeraciones)
        for _ in range(5)  # Puedes ajustar el tamaño de la población inicial según sea necesario
    ]

    ensamblaje_pc_genetico = EnsamblajePCGenetico(poblacion_inicial)
    mejor_ensamblaje = ensamblaje_pc_genetico.ejecutar_generaciones(100)

    resultado_label.config(text="Mejor ensamblaje de PC encontrado:\n" + mejor_ensamblaje.replace('|', '\n'))

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Optimización de Ensamblaje de PC")

frame = ttk.Frame(root, padding="20")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

boton_optimizar = ttk.Button(frame, text="Optimizar Ensamblaje", command=optimizar_ensamblaje)
boton_optimizar.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

resultado_label = ttk.Label(frame, text="")
resultado_label.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))

root.mainloop()
