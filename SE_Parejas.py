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
        genero = combo_Genero.get()
        edad = combo_Edad.get()
        orientacion_sex = combo_Orientacion.get()
        intereses = combo_Intereses.get()

        respuesta = text_respuesta.get("0.0", tk.END)
        explicacion = text_explicacion.get("0.0", tk.END)

        conexion = mysql.connector.connect(user='root',password='root',
                                        host='localhost',
                                        database='se_database',
                                        port='3306')
        print(conexion)
        cursor = conexion.cursor()
        # Valores para la base de datos
        valores = (genero, edad, orientacion_sex, intereses, respuesta, explicacion, imagen_blob)

        # Crea la consulta SQL para insertar un nuevo registro
        consulta = "INSERT INTO parejas(genero, edad, orientacion_sex, interes, resp, explicacion, img) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        # Ejecuta la consulta con los valores
        valores = (genero, edad, orientacion_sex, intereses, respuesta, explicacion, imagen_blob)
        cursor.execute(consulta, valores)

        # Confirma la inserción de datos en la base de datos
        conexion.commit()

        # Cierra el cursor y la conexión
        cursor.close()
        conexion.close()

    # ------------------------CARGAR IMAGEN--------------------- #
    def cargar_imagen():

        global imagen_blob
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.webp;*.png;*.jpg;*.jpeg;*.gif")])

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
    ventana_experto.title("Sistema Experto para escoger novio/a para tu hija/o")
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
    etiqueta_titulo = ttk.Label(ventana_experto, text="Sistema Experto escoger novio/a para tu hija/o:", font=fuente_Title)
    etiqueta_titulo.grid(row=0, column = 0, columnspan=2, pady=10)

    # Configurar las columnas para expandirse
    ventana_experto.columnconfigure(0, weight=1)
    ventana_experto.columnconfigure(1, weight=1)

    # Etiqueta y Combo Box para el Genero
    Genero = {
        "Masculino":"Ser humano que nacio Hombre y se identifica como tal",
        "Femenino": "Ser humano que nacio Mujer y se identifica como tal",
        "No binario": "Ser humano que nacio Hombre/Mujer pero ya no se identifica como tal"
    }
    etiqueta_Genero = ttk.Label(ventana_experto, text="¿Qué género es tu hijo?:")
    etiqueta_Genero.grid(row=1, column=0, padx=(20,0), pady=10, sticky="w")

    combo_Genero = ttk.Combobox(ventana_experto, values=list(Genero.keys()), state="readonly")
    combo_Genero.grid(row=1, column=0, padx=(147,0), pady=10, sticky ="w")

    # Etiqueta y Combo Box para la Edad
    Edad = { 
        "16-18": "Puberto",
        "19-24": "Adolescente",
        "25-30": "Adulto joven",
        "31-35": "Adulto"
    } 

    etiqueta_Edad = ttk.Label(ventana_experto, text="¿Que edad tiene su hijo/a?:")
    etiqueta_Edad.grid(row=2, column=0, padx=(20,0), pady=10, sticky ="w")

    combo_Edad = ttk.Combobox(ventana_experto, values=list(Edad.keys()), state="readonly")
    combo_Edad.grid(row=2, column=0, padx=(207,0), pady=10, sticky ="w")

    # Etiqueta y Combo Box para Orientación Sexual
    Orientacion_Sex = {
        "Heterosexual":"Heterosexual",
        "Bisexual":"Bisexual",
        "Homosexual":"Homosexual",
    }
    etiqueta_Orientacion = ttk.Label(ventana_experto, text="¿Que orientación sexual tiene tu hija/hijo?:")
    etiqueta_Orientacion.grid(row=3, column=0, padx=(20,0), pady=5, sticky ="w")

    combo_Orientacion = ttk.Combobox(ventana_experto, values=list(Orientacion_Sex.keys()), state="readonly")
    combo_Orientacion.grid(row=3, column=0, padx=(300,0), pady=5, sticky ="w")

    # Etiqueta y combo box para los Intereses
    Intereses = { 
        "Música":"Música",
        "Libros": "Libros",
        "Películas": "Películas",
        "Deportes": "Deportes",
        "Viajes": "Viajes",
        "Animales": "Animales"
    }
    etiqueta_Intereses = ttk.Label(ventana_experto, text="¿Que intereses tiene tu hija/o?:")
    etiqueta_Intereses.grid(row=5, column=0, padx=(20,0), pady=10, sticky ="w")

    combo_Intereses = ttk.Combobox(ventana_experto, values=list(Intereses.keys()), state="readonly")
    combo_Intereses.grid(row=5, column=0, padx=(224,0), pady=10, sticky ="w")

    # Boton Agregar Imagen
    boton_img = ttk.Button(ventana_experto, text="Subir imagen", command=cargar_imagen)
    boton_img.grid(row=6, column=0, padx=(370,0), pady= 5)

    # Crear la primera área de texto
    text_respuesta = scrolledtext.ScrolledText(ventana_experto, wrap=tk.WORD, width=42, height=5)
    text_respuesta.grid(row=7, column=0, padx=(20,0), pady=10, sticky ="w")

    # Crear la segunda área de texto debajo de la primera
    text_explicacion = scrolledtext.ScrolledText(ventana_experto, wrap=tk.WORD, width=42, height=5)
    text_explicacion.grid(row=8, column=0, padx=(20,0), pady=10, sticky ="w")

    # Definir el tamaño deseado
    nuevo_tamano = (200, 200)  # Cambia estos valores según tu preferenScia

    # Redimensionar la imagen
    imagen_redimensionada = imagen_pillow.resize(nuevo_tamano)

    # Convertir la imagen a formato Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

    # Crear un widget Label para mostrar la imagen
    etiqueta_imagen = tk.Label(ventana_experto, image=imagen_tk)
    etiqueta_imagen.grid(row=7, rowspan=2, column=0, padx=(380,0))

    # Botón para abrir modo usuario
    boton_modo_usuario = ttk.Button(ventana_experto, text="Regresar al modo usuario", command=abrir_ventana_usuario)
    boton_modo_usuario.grid(row=9, column=0, padx=(20,0), sticky ="w")

    # Botón para Guardar los Datos
    boton_guardar_datos = ttk.Button(ventana_experto, text="Guardar datos", command=guardar_en_base_de_hechos)
    boton_guardar_datos.grid(row=9, column=0, padx=(20,0))
    # ----------------------------CIERRE DE INTERFAZ DE USUARIO EXPERTO-----------------------------#=====================

def abrir_ventana_usuario():
    ventana_experto.destroy() # Cierra la ventana experto
    ventana.deiconify()  # Muestra la ventana principal


# ----------------------------INTERFAZ DE USUARIO NORMAL-----------------------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ventana = tk.Tk()
ventana.title("Sistema Experto para escoger novio/a para tu hija/o")
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
etiqueta_titulo = ttk.Label(ventana, text="Sistema Experto para escoger novio/a para tu hija/o:", font=fuente_Title)
etiqueta_titulo.grid(row=0, column = 0, columnspan=2, pady=10)

# Configurar las columnas para expandirse
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)

# Etiqueta y Combo Box para el Genero
Genero = {
    "Masculino":"Ser humano que nacio Hombre y se identifica como tal",
    "Femenino": "Ser humano que nacio Mujer y se identifica como tal",
    "No binario": "Ser humano que nacio Hombre/Mujer, pero ya no se identifica como tal"
}
etiqueta_Genero = ttk.Label(ventana_experto, text="¿Qué género es tu hijo?:")
etiqueta_Genero.grid(row=1, column=0, padx=(20,0), pady=10, sticky="w")

combo_Genero = ttk.Combobox(ventana_experto, values=list(Genero.keys()), state="readonly")
combo_Genero.grid(row=1, column=0, padx=(147,0), pady=10, sticky ="w")

# Etiqueta y Combo Box para la Edad
Edad = { 
    "16-18": "Puberto",
    "19-24": "Adolescente",
    "25-30": "Adulto joven",
    "31-35": "Adulto"
} 

etiqueta_Edad = ttk.Label(ventana_experto, text="¿Que edad tiene su hijo/a?:")
etiqueta_Edad.grid(row=2, column=0, padx=(20,0), pady=10, sticky ="w")

combo_Edad = ttk.Combobox(ventana_experto, values=list(Edad.keys()), state="readonly")
combo_Edad.grid(row=2, column=0, padx=(207,0), pady=10, sticky ="w")

# Etiqueta y Combo Box para Orientación Sexual
Orientacion_Sex = {
    "Heterosexual":"Heterosexual",
    "Bisexual":"Bisexual",
    "Homosexual":"Homosexual",
}
etiqueta_Orientacion = ttk.Label(ventana_experto, text="¿Que orientación sexual tiene tu hija/hijo?:")
etiqueta_Orientacion.grid(row=3, column=0, padx=(20,0), pady=5, sticky ="w")

combo_Orientacion = ttk.Combobox(ventana_experto, values=list(Orientacion_Sex.keys()), state="readonly")
combo_Orientacion.grid(row=3, column=0, padx=(300,0), pady=5, sticky ="w")

# Etiqueta y combo box para tiempo de los Intereses
Intereses = { # Cambier este noSQL por el que tenemos
    "Música":"Música",
    "Libros": "Libros",
    "Películas": "Películas",
    "Deportes": "Deportes",
    "Viajes": "Viajes",
    "Animales": "Animales"
}
etiqueta_Intereses = ttk.Label(ventana_experto, text="¿Que intereses tiene tu hija/o?:")
etiqueta_Intereses.grid(row=5, column=0, padx=(20,0), pady=10, sticky ="w")

combo_Intereses = ttk.Combobox(ventana_experto, values=list(Intereses.keys()), state="readonly")
combo_Intereses.grid(row=5, column=0, padx=(224,0), pady=10, sticky ="w")

# Crear la primera área de texto
text_respuesta = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=42, height=5, state=tk.DISABLED)
text_respuesta.grid(row=7, column=0, padx=(20,0), pady=10, sticky ="w")


# Crear la segunda área de texto debajo de la primera
text_explicacion = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=42, height=5, state=tk.DISABLED)
text_explicacion.grid(row=8, column=0, padx=(20,0), pady=10, sticky ="w")


# METODO PARA MOSTRAR LA EXPLICACION
def mostrar_explicacion():
    genero = combo_Genero.get()
    edad = combo_Edad.get()
    orientacion_sex = combo_Orientacion.get()
    intereses = combo_Intereses.get()

    conexion2 = mysql.connector.connect(user='root',password='root',
                                    host='localhost',
                                    database='se_database',
                                    port='3306')
    print(conexion2)
    cursor2 = conexion2.cursor()

    valores = (genero, edad, orientacion_sex, intereses)

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
    combo_Edad.set("")
    combo_Genero.set("")
    combo_Orientacion.set("")
    combo_Intereses.set("")
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
    genero = combo_Genero.get()
    edad = combo_Edad.get()
    orientacion_sex = combo_Orientacion.get()
    intereses = combo_Intereses.get()

    # CONEXION CON LA BD PARA VER SI COINCIDEN LOS DATOS CON ALGO YA GUARDADO
    conexion3 = mysql.connector.connect(user='root',password='root',
                                    host='localhost',
                                    database='se_database',
                                    port='3306')
    print(conexion3)
    cursor3 = conexion3.cursor()

    valores = (genero, edad, orientacion_sex, intereses)

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
    genero = combo_Genero.get()
    edad = combo_Edad.get()
    orientacion_sex = combo_Orientacion.get()
    intereses = combo_Intereses.get()

    # CONEXION CON LA BD PARA VER SI COINCIDEN LOS DATOS CON ALGO YA GUARDADO
    conexion2 = mysql.connector.connect(user='root',password='root',
                                    host='localhost',
                                    database='se_database',
                                    port='3306')
    print(conexion2)
    cursor2 = conexion2.cursor()

    valores = (genero, edad, orientacion_sex, intereses)

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