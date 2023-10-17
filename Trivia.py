import tkinter as tk
from tkinter import IntVar, ttk
from tkinter import messagebox
import tkinter.font as tkFont
import mysql.connector
import time

# Preguntas:
# Como hago para que no comiencen seleccionados los radio buttons? Ya probe declarando como None la variable var, y si la declaro en el bucle como IntVar no anda directamente
# Como hago para que me impida seguir si no seleccione ninguna respuesta? funcion verificar respuesta()
# Utilize ventana_secundaria.quit y me sacaba de la pantalla principal al finalizar. Ahora con withdraw se esconde y hay que reiniciar, pero sigue rompiendo al cerrar la secundaria y volver a querer jugar. Lo mismo pasa con el boton cerrar ventana
# Como actualizo el reloj? ya probe que al reiniciar juego llame a iniciar_reloj o a actualizar_reloj
#

conexion = mysql.connector.connect(host="127.0.0.1", user="root", password="Martin*30",port=3305 ,database="Trivia")

cursor = conexion.cursor()

def cargar_datos():
    tree.delete(*tree.get_children())
    cursor = conexion.cursor()
    cursor.execute(" Usuario.IdUsuario, Usuario.Nombre, Usuario.Instagram, Usuario.Puntaje, Usuario.Tiempo, Pregunta.IdPregunta, Pregunta.Pregunta, Pregunta.Respuesta, Pregunta.Puntaje_pregunta FROM Usuario JOIN Puntaje ON Usuario.IdUsuario = Pregunta.Puntaje_pregunta")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def iniciar_reloj():
    global tiempo_segundos
    tiempo_segundos = 0
    actualizar_reloj()

def actualizar_reloj():
    global tiempo_segundos
    horas = tiempo_segundos // 3600
    minutos = (tiempo_segundos % 3600) // 60
    segundos = tiempo_segundos % 60
    tiempo_formateado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    reloj.config(text=tiempo_formateado)
    tiempo_segundos += 1
    ventana.after(1000, actualizar_reloj)

def reiniciar_juego():
    global respuestas_correctas, indice_pregunta_actual
    respuestas_correctas = 0
    indice_pregunta_actual = 0
    mostrar_pregunta()
    actualizar_puntaje()

def nuevo_usuario():
    usuario = usuario_entry.get().upper()
    instagram = instagram_entry.get().upper()
    tiempo = tiempo_segundos
    if usuario == "" or instagram == "":
        messagebox.showerror("Error", "Por favor, ingresa usuario e Instagram.")
        return
    query = "INSERT INTO Usuario (Nombre, Instagram, Tiempo) VALUES (%s, %s, %s)"
    data = (usuario, instagram, tiempo)
    cursor.execute(query, data)
    conexion.commit()
    cargar_datos()
    usuario_entry.delete(0, tk.END)
    instagram_entry.delete(0, tk.END)
    messagebox.showinfo("Gracias", "Estos datos son suficientes para hackearte")

def logros():
    tree.delete(*tree.get_children())
    cursor = conexion.cursor()
    

# Preguntas y respuestas
preguntas_respuestas = [
    {
        "pregunta": "¿En que fecha se creo el instituto?",
        "opciones": ["2", "1982", "2018", "1000 A.C"],
        "respuesta_correcta": "1982"
    },
    {
        "pregunta": "¿Cuantos alumnos hay en 2do de Software?",
        "opciones": ["300", "2", "15", "35"],
        "respuesta_correcta": "15"
    },
    {
        "pregunta": "¿Que dia es hoy?",
        "opciones": ["Lunes", "Martes", "Miercoles", "Jueves"],
        "respuesta_correcta": "Lunes"
    }
]

# Variables globales
indice_pregunta_actual = 0
respuestas_correctas = 0

def abrir_ventana_secundaria():
    ventana_secundaria.deiconify()  # Mostrar la ventana secundaria

def abrir_ventana_logros():
    ventana_logros.deiconify()

def verificar_respuesta():
    global indice_pregunta_actual, respuestas_correctas
    respuesta_seleccionada = var.get()
    respuesta_correcta = preguntas_respuestas[indice_pregunta_actual]["respuesta_correcta"]
    
    if var == None:
        messagebox.showinfo("Advertencia", "Debes seleccionar una opción para continuar")      #gasdaysdsaydgdgayagdiagdyasvdayvfyasvfyasvfauisfvaisy

    if respuesta_seleccionada == respuesta_correcta:
        respuestas_correctas += 1
    
    indice_pregunta_actual += 1
    
    if indice_pregunta_actual < len(preguntas_respuestas):
        mostrar_pregunta()
    else:
        messagebox.showinfo("Fin del juego", f"Tu puntaje final es: {respuestas_correctas}/{len(preguntas_respuestas)}")
        ventana_secundaria.withdraw()
        reiniciar_juego()

    # Mostrar puntaje actual después de cada pregunta
    actualizar_puntaje()

def mostrar_pregunta():
    pregunta_label.config(text=preguntas_respuestas[indice_pregunta_actual]["pregunta"])
    for i in range(4):
        radio_botones[i].config(text=preguntas_respuestas[indice_pregunta_actual]["opciones"][i], value=preguntas_respuestas[indice_pregunta_actual]["opciones"][i])
        var_opciones[i].set("")

# Actualizar el puntaje mostrado en la ventana
def actualizar_puntaje():
    puntaje_label.config(text=f"Respuestas correctas: {respuestas_correctas}/{len(preguntas_respuestas)}")

# Configuración de la ventana principal
ventana = tk.Tk()
# Obtener el ancho y alto de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
"""
# Establecer las dimensiones de la ventana para que coincidan con la pantalla
ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}") """
ventana.wm_state("zoomed")
ventana.config(bg="#0b4f64")
ventana.title("Trivia Game")
fontStyle = tkFont.Font(family="Lucida Grande", size=20)

# Agregar la imagen a la ventana principal
image = tk.PhotoImage(file="ISAUILogo.png")
label_Imag = ttk.Label(ventana, image=image)
label_Imag.pack(side=tk.TOP)

label_usuario = ttk.Label(ventana, text="Usuario",font=("Lucida Grande", 12))
label_usuario.place(x=150, y=400, width=75, height=50)
usuario_entry = tk.Entry(ventana,font=("Lucida Grande", 12))
usuario_entry.place(x=250, y=405, width=300, height=40)
label_instagram = ttk.Label(ventana, text="Instagram",font=("Lucida Grande", 12))
label_instagram.place(x=150, y=525, width=75, height=50)
instagram_entry = tk.Entry(ventana,font=("Lucida Grande", 12))
instagram_entry.place(x=250, y=530, width=300, height=40)

""" def timer():
    tiempo_actal = time.strftime("%H:%M:%S")
    reloj.config(text = tiempo_actal)
    ventana.after(1000, timer)"""

jugar_boton = tk.Button(ventana, text="Jugar", command= lambda:[abrir_ventana_secundaria() , iniciar_reloj()], padx=10, pady=15, font=fontStyle)
jugar_boton.place(relx=0.5,rely=0.5,width=270,anchor='c')
jugar_boton.config(fg="black", bg="#ffffff")
guardar_button = tk.Button(ventana, text="Guardar", command=nuevo_usuario)
guardar_button.place(x=600, y=465, width=75, height=50)

# Crear una ventana secundaria.
ventana_secundaria = tk.Toplevel()

# Obtener el ancho y alto de la pantalla
ancho_pantalla_secundaria = ventana_secundaria.winfo_screenwidth()
alto_pantalla_secundaria = ventana_secundaria.winfo_screenheight()

# Establecer las dimensiones de la ventana para que coincidan con la pantalla
ventana_secundaria.geometry(f"{ancho_pantalla}x{alto_pantalla}")
ventana_secundaria.title("Juego")
ventana_secundaria.withdraw()  # Ocultar la ventana secundaria inicialmente

boton_cerrar = ttk.Button(
    ventana_secundaria,
    text="Cerrar ventana", 
    command=ventana_secundaria.withdraw)
boton_cerrar.place(x=600, y=550)    

# Etiqueta de la pregunta
pregunta_label = tk.Label(ventana_secundaria, text="", padx=10, pady=40, font=fontStyle)
pregunta_label.pack()

#Timer
reloj = tk.Label(ventana_secundaria, font=("Arial", 20), bg="#0b4f64", fg="#ffffff")

reloj.place(x=50, y=200, width=150, height=100)

# Variables para almacenar la respuesta seleccionada
var = tk.StringVar()

# Variables de control para los botones de radio
var_opciones = [tk.StringVar() for _ in range(4)]

# Radio botones para las opciones de respuesta
radio_botones = []
for i in range(4):
    radio_boton = tk.Radiobutton(ventana_secundaria,text="", variable=var, value="", padx=10, pady=5, font=fontStyle, state="normal")
    radio_boton.pack()
    radio_botones.append(radio_boton)
    
# Etiqueta para mostrar el puntaje
puntaje_label = tk.Label(ventana_secundaria, text="Respuestas correctas: 0/0", padx=10, pady=25, font=fontStyle)
puntaje_label.pack()

# Botón para verificar respuesta
verificar_boton = tk.Button(ventana_secundaria, text="Verificar respuesta", command=verificar_respuesta, padx=10, pady=15, font=fontStyle)
verificar_boton.pack()
verificar_boton.config(fg="black", bg="lightblue")

#  Ventana terciara o de logros
ventana_logros = tk.Toplevel()
ancho_pantalla_logros = ventana_logros.winfo_screenwidth()
alto_pantalla_logros = ventana_logros.winfo_screenheight()
ventana_logros.geometry(f"{ancho_pantalla}x{alto_pantalla}")
ventana_logros.title("Logros")
ventana_logros.withdraw()

# Crear Treeview para mostrar la información
tree = ttk.Treeview(ventana_logros, columns=("Id","Nombre", "Instagram", "Tiempo"))
tree.heading("#1", text="Id")
tree.heading("#2", text="Nombre")
tree.heading("#3", text="Instagram")
tree.heading("#4", text="Tiempo")

tree.column("#0", width=0, stretch=tk.NO)  # Ocultar la columna #0 que habitualmente muestra las primary key de los objetos

tree.pack(padx=10, pady=10)

# Iniciar el juego
mostrar_pregunta()

reiniciar_juego()

ventana.mainloop()

"""
Rompe:

* Apretar jugar y cerrar la ventana, no me deja jugar nuevamente
* Todavia no guarda usuario e ig en BDD
* Todavia las preguntas no estan en BDD
* Se seleccionan todos los circulos al comenzar

"""