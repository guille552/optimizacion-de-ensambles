from io import BytesIO
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import mysql.connector
from tkinter import ttk
from PIL import Image, ImageTk

# MÉTODO PARA ABRIR LA VENTANA EXPERTO
ventana_experto = None
def abrir_ventana_experto():
    #MÉTODO PARA GUARDAR EN LA BASE DE HECHOS
    def guardar_en_base_de_hechos():

        global imagen_blob
        componente = combo_Componente.get()
        marca = combo_Marca.get()
        modelo = combo_Modelo.get()
        especificaciones = text_Especificaciones.get("0.0", tk.END)
        precio = text_Precio.get("0.0", tk.END)

        conexion = mysql.connector.connect(user='root', password='root',
                                           host='localhost',
                                           database='se_database',
                                           port='3306')
        cursor = conexion.cursor()
        # Valores para la base de datos
        valores = (componente, marca, modelo, especificaciones, precio, imagen_blob)

        # Crea la consulta SQL para insertar un nuevo registro
        consulta = "INSERT INTO componentes(componente, marca, modelo, especificaciones, precio, imagen) VALUES (%s,%s,%s,%s,%s,%s)"

        # Ejecuta la consulta con los valores
        cursor.execute(consulta, valores)

        # Confirma la inserción de datos en la base de datos
        conexion.commit()

        # Cierra el cursor y la conexión
        cursor.close()
        conexion.close()

    # ------------------------CARGAR IMAGEN--------------------- #
    def cargar_imagen():

        global imagen_blob
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", ".webp;.png;.jpg;.jpeg;*.gif")])

        if ruta_imagen:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((200, 200))  # Ajusta el tamaño de la imagen según tus necesidades
            imagen_tk = ImageTk.PhotoImage(imagen)

            # Convertir la imagen a formato BLOB
            buffer = BytesIO()
            imagen.save(buffer, format="JPEG")  # El formato se obtiene automáticamente del original
            imagen_blob = buffer.getvalue()

            etiqueta_imagen.config(image=imagen_tk)
            etiqueta_imagen.image = imagen_tk  # ¡Importante! Evita que la imagen se elimine debido a la recolección de basura


    # ----------------------------INTERFAZ DE USUARIO EXPERTO-----------------------------#==================
    global ventana_experto
    ventana.withdraw()  # Oculta la ventana principal
    ventana_experto = tk.Toplevel(ventana)  # Crea una nueva ventana secundaria
    ventana_experto.title("Ensamblaje de PC")
    ancho_ventana = 625
    alto_ventana = 500

    # Obtener el ancho y alto de la pantalla
    ancho_pantalla = ventana_experto.winfo_screenwidth()
    alto_pantalla = ventana_experto.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana
    x_pos = (ancho_pantalla - ancho_ventana) // 2
    y_pos = (alto_pantalla - alto_ventana) // 2

    # Configurar la geometría de la ventana
    ventana_experto.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    # Interfaz de Usuario
    fuente_Title = ('Arial', 15)  # Tipo de letra Arial, tamaño 16

    # Titulo
    etiqueta_titulo = ttk.Label(ventana_experto, text="Ensamblaje de PC:", font=fuente_Title)
    etiqueta_titulo.grid(row=0, column=0, columnspan=2, pady=10)

    # Configurar las columnas para expandirse
    ventana_experto.columnconfigure(0, weight=1)
    ventana_experto.columnconfigure(1, weight=1)

    # Etiqueta y Combo Box para el Componente
    componentes = ["Procesador", "Tarjeta Gráfica", "Memoria RAM", "Almacenamiento", "Fuente de Poder", "Placa Base"]
    etiqueta_Componente = ttk.Label(ventana_experto, text="Componente:")
    etiqueta_Componente.grid(row=1, column=0, padx=(20,0), pady=10, sticky="w")

    combo_Componente = ttk.Combobox(ventana_experto, values=componentes, state="readonly")
    combo_Componente.grid(row=1, column=1, padx=(20,0), pady=10, sticky="w")

    # Etiqueta y Combo Box para la Marca
    marcas = ["Intel", "AMD", "NVIDIA", "Corsair", "ASUS"]
    etiqueta_Marca = ttk.Label(ventana_experto, text="Marca:")
    etiqueta_Marca.grid(row=2, column=0, padx=(20,0), pady=10, sticky="w")

    combo_Marca = ttk.Combobox(ventana_experto, values=marcas, state="readonly")
    combo_Marca.grid(row=2, column=1, padx=(20,0), pady=10, sticky="w")

    # Etiqueta y Combo Box para el Modelo
    modelos = ["Core i9", "Ryzen 9", "RTX 3090", "GTX 1660", "DDR4", "DDR3", "SSD", "HDD", "1000W", "750W", "Z490", "B450"]
    etiqueta_Modelo = ttk.Label(ventana_experto, text="Modelo:")
    etiqueta_Modelo.grid(row=3, column=0, padx=(20,0), pady=10, sticky="w")

    combo_Modelo = ttk.Combobox(ventana_experto, values=modelos, state="readonly")
    combo_Modelo.grid(row=3, column=1, padx=(20,0), pady=10, sticky="w")

    # Etiqueta y área de texto para Especificaciones
    etiqueta_Especificaciones = ttk.Label(ventana_experto, text="Especificaciones:")
    etiqueta_Especificaciones.grid(row=4, column=0, padx=(20,0), pady=10, sticky="w")

    text_Especificaciones = scrolledtext.ScrolledText(ventana_experto, wrap=tk.WORD, width=42, height=5)
    text_Especificaciones.grid(row=4, column=1, padx=(20,0), pady=10, sticky="w")

    # Etiqueta y área de texto para Precio
    etiqueta_Precio = ttk.Label(ventana_experto, text="Precio:")
    etiqueta_Precio.grid(row=5, column=0, padx=(20,0), pady=10, sticky="w")

    text_Precio = scrolledtext.ScrolledText(ventana_experto, wrap=tk.WORD, width=42, height=1)
    text_Precio.grid(row=5, column=1, padx=(20,0), pady=10, sticky="w")

    # Botón para cargar imagen
    boton_img = ttk.Button(ventana_experto, text="Subir imagen", command=cargar_imagen)
    boton_img.grid(row=6, column=0, padx=(370,0), pady=5)

    # Crear un widget Label para mostrar la imagen
    etiqueta_imagen = tk.Label(ventana_experto)
    etiqueta_imagen.grid(row=7, column=0, rowspan=2, padx=(380,0), pady=5)

    # Botón para guardar los datos
    boton_guardar_datos = ttk.Button(ventana_experto, text="Guardar datos", command=guardar_en_base_de_hechos)
    boton_guardar_datos.grid(row=9, column=0, padx=(20,0))

    # Botón para regresar al modo usuario
    boton_modo_usuario = ttk.Button(ventana_experto, text="Regresar al modo usuario", command=abrir_ventana_usuario)
    boton_modo_usuario.grid(row=9, column=1, padx=(20,0))

def abrir_ventana_usuario():
    ventana_experto.destroy()  # Cierra la ventana experto
    ventana.deiconify()  # Muestra la ventana principal

# ----------------------------INTERFAZ DE USUARIO NORMAL-----------------------------#~~~~~~~~~~~

ventana = tk.Tk()
ventana.title("Ensamblaje de PC")
ancho_ventana = 625
alto_ventana = 500

# Obtener el ancho y alto de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x_pos = (ancho_pantalla - ancho_ventana) // 2
y_pos = (alto_pantalla - alto_ventana) // 2

# Configurar la geometría de la ventana
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Interfaz de Usuario
fuente_Title = ('Arial', 18)  # Tipo de letra Arial, tamaño 16

# Titulo
etiqueta_titulo = ttk.Label(ventana, text="Ensamblaje de PC", font=fuente_Title)
etiqueta_titulo.grid(row=0, column = 0, columnspan=2, pady=10)

# Configurar las columnas para expandirse
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)

# Etiqueta y Combo Box para el Genero
Marca = {
    "Intel":"Marca para procesadores Intel",
    "AMD" : "Marca para procesadores AMD"
}
etiqueta_Marca = ttk.Label(ventana_experto, text="¿Qué marca prefiere?")
etiqueta_Marca.grid(row=1, column=0, padx=(20,0), pady=10, sticky="w")

combo_Marca = ttk.Combobox(ventana_experto, values=list(Marca.keys()), state="readonly")
combo_Marca.grid(row=1, column=0, padx=(147,0), pady=10, sticky ="w")

# Etiqueta y Combo Box para la Edad
Presupuesto = { 
    "5000-8000": "Bajo",
    "8000-12000": "Medio",
    "12000-20000": "Alto",
    "No importa el presupuesto": "Ilimitado"
} 

etiqueta_Presupuesto = ttk.Label(ventana_experto, text="¿Que presupuesto tiene?:")
etiqueta_Presupuesto.grid(row=2, column=0, padx=(20,0), pady=10, sticky ="w")

combo_Presupuesto = ttk.Combobox(ventana_experto, values=list(Presupuesto.keys()), state="readonly")
combo_Presupuesto.grid(row=2, column=0, padx=(207,0), pady=10, sticky ="w")

# Etiqueta y Combo Box para Orientación Sexual
Uso = {
    "Gaming":"Dedicado a juegos",
    "Arquitectura":"Dedicado a diseño arquitectónico",
    "Diseño gráfico":"Dedicado a diseño gráfico"
}
etiqueta_Uso = ttk.Label(ventana_experto, text="¿Que uso le dará a su PC?:")
etiqueta_Uso.grid(row=3, column=0, padx=(20,0), pady=5, sticky ="w")

combo_Uso = ttk.Combobox(ventana_experto, values=list(Uso.keys()), state="readonly")
combo_Uso.grid(row=3, column=0, padx=(300,0), pady=5, sticky ="w")

# Crear la primera área de texto
text_respuesta = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=42, height=5, state=tk.DISABLED)
text_respuesta.grid(row=7, column=0, padx=(20,0), pady=10, sticky ="w")


# Crear la segunda área de texto debajo de la primera
text_explicacion = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=42, height=5, state=tk.DISABLED)
text_explicacion.grid(row=8, column=0, padx=(20,0), pady=10, sticky ="w")


# METODO PARA MOSTRAR LA EXPLICACION
def mostrar_explicacion():
    marca = combo_Marca.get()
    presupuesto = combo_Presupuesto.get()
    uso = combo_Uso.get()


    conexion2 = mysql.connector.connect(user='root',password='root',
                                    host='localhost',
                                    database='se_database',
                                    port='3306')
    print(conexion2)
    cursor2 = conexion2.cursor()

    valores = (marca, presupuesto, uso)

    # Crea la consulta SQL para rescatar una imagen
    consulta_existencia = "SELECT explicacion FROM parejas WHERE genero = %s AND edad = %s AND orientacion_sex = %s AND interes = %s"

    # Ejecuta la consulta con los valores
    cursor2.execute(consulta_existencia, valores)

    # Verificar si hay algún resultado
    resultados = cursor2.fetchall()

    # Limpiar el contenido actual del text_respuesta
    text_explicacion.config(state=tk.NORMAL)
    text_explicacion.delete('1.0', tk.END)

    for resultado in resultados:
        explicacion, = resultado
        print(explicacion)

        # Establecer un valor inicial
        text_explicacion.insert(tk.END, f"Es una pareja pontencial ya que: {explicacion}\nNota: Las parejas mostradas por este sistema no asegura al 100% la compatibilidad afectiva, ni tampoco el que las conozcas.") #Cambiar
        break
    else:
        print("No hay nada")

    # Confirma la inserción de datos en la base de datos
    conexion2.commit()

    # Cierra el cursor y la conexión
    cursor2.close()
    conexion2.close()

    # Configurar el text_respuesta como de solo lectura
    text_explicacion.config(state=tk.DISABLED)



# LIMPIA LAS CASILLAS CUANDO SE QUIERE REALIZAR OTRA CONSULTA
def limpiar_casillas():
    combo_Marca.set("")
    combo_Presupuesto.set("")
    combo_Uso.set("")
    text_explicacion.config(state=tk.NORMAL)
    text_explicacion.delete('1.0', tk.END)
    text_explicacion.insert(tk.END, "")
    text_explicacion.config(state=tk.DISABLED)
    text_respuesta.config(state=tk.NORMAL)
    text_respuesta.delete('1.0', tk.END)
    text_respuesta.insert(tk.END, "")
    text_respuesta.config(state=tk.DISABLED)


imagen_pillow = Image.open("Logo.webp")

# Definir el tamaño deseado
nuevo_tamano = (200, 200)  # Cambia estos valores según tu preferencia

# Redimensionar la imagen
imagen_redimensionada = imagen_pillow.resize(nuevo_tamano)

# Convertir la imagen a formato Tkinter
imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

# Crear un widget Label para mostrar la imagen
etiqueta_imagen = tk.Label(ventana, image=imagen_tk)
etiqueta_imagen.grid(row=7, rowspan=2, column=0, padx=(380,0))

# MÉTODO PARA MOSTRAR LA IMAGEN
def obtener_img():
    marca = combo_Marca.get()
    presupuesto = combo_Presupuesto.get()
    uso = combo_Uso.get()
    # CONEXION CON LA BD PARA VER SI COINCIDEN LOS DATOS CON ALGO YA GUARDADO
    conexion3 = mysql.connector.connect(user='root',password='root',
                                    host='localhost',
                                    database='se_database',
                                    port='3306')
    print(conexion3)
    cursor3 = conexion3.cursor()

    valores = (marca, presupuesto, uso)

    consulta_imagen = "SELECT img FROM parejas WHERE genero = %s AND edad = %s AND orientacion_sex = %s AND interes = %s"

    # Ejecuta la consulta con los valores
    cursor3.execute(consulta_imagen, valores)

    # Verificar si hay algún resultado
    resultadoImg = cursor3.fetchone()

    if resultadoImg is not None:

        imagen_bytes2 = resultadoImg[0]

        # Abrir la imagen con Pillow
        imagen_pillow2 = Image.open(BytesIO(imagen_bytes2))

        # Redimensionar la imagen
        imagen_redimensionada2 = imagen_pillow2.resize(nuevo_tamano)

        # Convertir la imagen a formato Tkinter
        imagen_tk2 = ImageTk.PhotoImage(imagen_redimensionada2)

        # Actualizar la imagen en el widget Label
        etiqueta_imagen.config(image=imagen_tk2)

        # Mantener la referencia global a la imagen_tk para evitar que sea eliminada
        etiqueta_imagen.image = imagen_tk2
    else:

        imagen_pillow = Image.open("Logo.webp")

        # Redimensionar la imagen
        imagen_redimensionada2 = imagen_pillow.resize(nuevo_tamano)

        # Convertir la imagen a formato Tkinter
        imagen_tk2 = ImageTk.PhotoImage(imagen_redimensionada2)

        # Actualizar la imagen en el widget Label
        etiqueta_imagen.config(image=imagen_tk2)

        # Mantener la referencia global a la imagen_tk para evitar que sea eliminada
        etiqueta_imagen.image = imagen_tk2


    # Confirma la inserción de datos en la base de datos
    conexion3.commit()

    # Cierra el cursor y la conexión
    cursor3.close()
    conexion3.close()
    ventana.update()

def llamar_funciones():
    obtener_consulta()
    obtener_img()



# MÉTODO PARA MOSTRAR LA RESPUESTA
def obtener_consulta():
    marca = combo_Marca.get()
    presupuesto = combo_Presupuesto.get()
    uso = combo_Uso.get()

    # CONEXION CON LA BD PARA VER SI COINCIDEN LOS DATOS CON ALGO YA GUARDADO
    conexion2 = mysql.connector.connect(user='root',password='root',
                                    host='localhost',
                                    database='se_database',
                                    port='3306')
    print(conexion2)
    cursor2 = conexion2.cursor()

    valores = (marca, presupuesto, uso)

    consulta_existencia = "SELECT resp FROM parejas WHERE genero = %s AND edad = %s AND orientacion_sex = %s AND interes = %s"

    # Ejecuta la consulta con los valores
    cursor2.execute(consulta_existencia, valores)

    # Verificar si hay algún resultado
    resultados = cursor2.fetchall()

    # Limpiar el contenido actual del text_respuesta
    text_respuesta.config(state=tk.NORMAL)
    text_respuesta.delete('1.0', tk.END)

    for resultado in resultados:
        pareja, = resultado

        # Establecer un valor inicial
        text_respuesta.insert(tk.END, f"Según los datos ingresados, una potencial pareja puede ser: {pareja}")

        text_explicacion.config(state=tk.NORMAL)
        text_explicacion.delete('1.0', tk.END)
        text_explicacion.insert(tk.END, "")
        text_explicacion.config(state=tk.DISABLED)

        break
    else:
        text_respuesta.insert(tk.END, f"No se encontró ninguna posible pareja en la base de datos.")
        text_explicacion.config(state=tk.NORMAL)
        text_explicacion.delete('1.0', tk.END)
        text_explicacion.insert(tk.END, "")
        text_explicacion.config(state=tk.DISABLED)

    conexion2.commit()

    # Cierra el cursor y la conexión
    cursor2.close()
    conexion2.close()

    # Configurar el text_respuesta como de solo lectura
    text_respuesta.config(state=tk.DISABLED)


# Boton Obtener consulta
boton_consultar = ttk.Button(ventana, text="Obtener consulta", command=llamar_funciones)
boton_consultar.grid(row=6, column=0, sticky ="w", pady= 5, padx=(200,0))

# Boton Ver Explicación
boton_consultar = ttk.Button(ventana, text="Ver explicación", command=mostrar_explicacion)
boton_consultar.grid(row=6, column=0, sticky ="e", pady= 5, padx=(0,160))

# Botón realizar otra consulta
boton_realizar_consulta = ttk.Button(ventana, text="Realizar otra consulta",command=limpiar_casillas)
boton_realizar_consulta.grid(row=9, column=0, padx=(20,0), sticky ="w")

# Botón para abrir ventana experto
boton_abrir_experto = ttk.Button(ventana, text="Entrar a Modo Experto", command=abrir_ventana_experto)
boton_abrir_experto.grid(row=9, column=0, padx=(20,0))

ventana.mainloop()