import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import mysql.connector
import random

#probar con este

conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Martin*30",
    port=3305,
    database="Trivia"
)

temporizador_reloj = None
cursor = conexion.cursor()
indice_pregunta_actual = 0
respuestas_correctas = 0
puntaje = 0
tiempo_transcurrido = 0 

preguntas = []
pregunta_actual = None


def cargar_preguntas():
    if not preguntas:  # Solo carga preguntas si la lista está vacía
        cursor.execute("SELECT * FROM Preguntas")
        for pregunta in cursor.fetchall():
            preguntas.append(pregunta)

def cargar_usuario():
    tree.delete(*tree.get_children())
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Usuarios ORDER BY Usuarios.id DESC ")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row) 

def mostrar_alerta(mensaje):
    messagebox.showwarning("Alerta", mensaje)

def dejar_jugar():
    global indice_pregunta_actual, respuestas_correctas, puntaje
    if usuario_entry.get() and instagram_entry.get():
        cargar_preguntas()
        indice_pregunta_actual = 0  # Inicializar la variable
        respuestas_correctas = 0  # Reiniciar el contador de respuestas correctas
        mostrar_siguiente_pregunta()
        iniciar_reloj()
        guardar_usuario()
        abrir_ventana_secundaria()
        usuario_entry.delete(0, tk.END)
        instagram_entry.delete(0, tk.END)
        puntaje = 0
    else:
        mostrar_alerta("Para jugar, debes ingresar tu nombre de usuario e Instagram")

def guardar_usuario():
    global puntaje, tiempo_segundos
    cursor = conexion.cursor()
    nombre = usuario_entry.get().upper()
    instagram = instagram_entry.get()
    cursor.execute("INSERT INTO Usuarios (Nombre, Instagram, Puntaje, Tiempo) VALUES (%s,%s,%s,%s)", (nombre, instagram, puntaje,tiempo_transcurrido))
    conexion.commit()
    cargar_usuario()
    usuario_entry.delete(0, tk.END)
    instagram_entry.delete(0, tk.END)
    if nombre and instagram:
        pass
    else:
        mostrar_alerta("Los campos son obligatorios. Debes completarlos")

reloj = None  # Agrega esta línea fuera de cualquier función para definir reloj

def abrir_ventana_secundaria():
    ventana_secundaria.deiconify()  # Mostrar la ventana secundaria
    global reloj  # Debes usar global para modificar la variable en la función

def iniciar_reloj():
    global tiempo_segundos, temporizador_reloj
    tiempo_segundos = 0
    tiempo_transcurrido = 0  # Reiniciar la variable de tiempo transcurrido
    if temporizador_reloj is not None:
        ventana.after_cancel(temporizador_reloj)
    actualizar_reloj()

def actualizar_reloj():
    global tiempo_segundos, temporizador_reloj, tiempo_transcurrido
    horas = tiempo_segundos // 3600
    minutos = (tiempo_segundos % 3600) // 60
    segundos = tiempo_segundos % 60
    tiempo_formateado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    
    if reloj is not None:
        reloj.config(text=tiempo_formateado)
        tiempo_segundos += 1
        tiempo_transcurrido += 1  # Actualizar el tiempo transcurrido
        temporizador_reloj = ventana.after(1000, actualizar_reloj)

def verificar_respuesta():
    global respuestas_correctas, indice_pregunta_actual, puntaje
    pregunta_actual = preguntas[indice_pregunta_actual - 1]
    respuesta_correcta = pregunta_actual[2]

    if respuesta_seleccionada == respuesta_correcta:
        respuestas_correctas += 1
        puntaje += 100

    indice_pregunta_actual -= 1  # Restar 1 al índice de la pregunta actual
    mostrar_siguiente_pregunta()


def finalizar_juego():
    ventana_secundaria.withdraw()
    mostrar_alerta(f"Juego terminado. Respuestas correctas: {respuestas_correctas}/{len(preguntas)}")


def mostrar_siguiente_pregunta():
    global pregunta_actual, indice_pregunta_actual, respuesta_seleccionada,puntaje

    if indice_pregunta_actual < len(preguntas):
        pregunta_actual = preguntas[indice_pregunta_actual]
        pregunta_label.config(text=pregunta_actual[1])

        opciones = [pregunta_actual[2], pregunta_actual[3], pregunta_actual[4], pregunta_actual[5]]
        random.shuffle(opciones)

        for i in range(4):
            labels_respuesta[i].config(text=opciones[i])

        respuesta_seleccionada = None  # Reiniciar la respuesta seleccionada
        indice_pregunta_actual += 1
    else:
        finalizar_juego()

def seleccionar_respuesta(respuesta):
    global respuesta_seleccionada
    respuesta_seleccionada = labels_respuesta[respuesta - 1].cget("text") # -1 porque la respuesta seleccionada no coincide con el numero de indice de la respuesta correcta en la bbd
    verificar_respuesta()
    mostrar_siguiente_pregunta()

def abrir_ventana_logros():
    ventana_logros.deiconify()

ventana = tk.Tk()
ventana.title("Trivia Game")
fontStyle = tkFont.Font(family="Lucida Grande", size=20)
ventana.wm_state("zoomed")
ventana.config(bg="#0b4f64")

ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

style = ttk.Style()
style.configure("BW.TLabel", background="#0b4f64",foreground="white")

image = tk.PhotoImage(file="ISAUI_40.png")
label_Imag = ttk.Label(ventana, image=image)
label_Imag.pack(side=tk.TOP) 

label_usuario = ttk.Label(ventana, text="Usuario", style="BW.TLabel",font=("Lucida Grande", 15))
label_usuario.place(x=150, y=400, width=75, height=50)
usuario_entry = tk.Entry(ventana, font=("Lucida Grande", 12))
usuario_entry.place(x=250, y=405, width=300, height=40)
label_instagram = ttk.Label(ventana, text="Instagram", style="BW.TLabel",font=("Lucida Grande", 15))
label_instagram.place(x=120, y=525, width=100, height=50)
instagram_entry = tk.Entry(ventana, font=("Lucida Grande", 12))
instagram_entry.place(x=250, y=530, width=300, height=40)

jugar_boton = tk.Button(ventana, text="Jugar", command=dejar_jugar, padx=10, pady=15, font=fontStyle)
jugar_boton.place(relx=0.5, rely=0.5, width=270, anchor='c')
jugar_boton.config(fg="black", bg="#ffffff",relief="sunken")


ventana_secundaria = tk.Toplevel()
ventana_secundaria.geometry(f"{ventana.winfo_screenwidth()}x{ventana.winfo_screenheight()}")
ventana_secundaria.title("Juego")
ventana_secundaria.withdraw()
ventana_secundaria.config(bg="#0b4f64")
ventana_secundaria.overrideredirect(True)

boton_cerrar = tk.Button(
    ventana_secundaria,
    text="Cerrar ventana", 
    command=ventana_secundaria.withdraw,
    font=fontStyle)
boton_cerrar.place(x=1000, y=650)    


reloj = tk.Label(ventana_secundaria, font=("Arial", 20), bg="#0b4f64", fg="#ffffff")
reloj.place(x=1100, y=200, width=150, height=100)

pregunta_label = tk.Label(ventana_secundaria, text="", padx=10, pady=40, font=fontStyle)
pregunta_label.config(bg="#0b4f64", fg="#ffffff")
pregunta_label.pack()

labels_respuesta = []
for i in range(4):
    label = tk.Label(ventana_secundaria, text="", padx=10, pady=10, font=fontStyle)
    label.config(bg="#0b4f64", fg="white")
    label.pack()
    labels_respuesta.append(label)

    label_numero = tk.Label(ventana_secundaria, text=str(i+1), font=fontStyle)
    label_numero.config(bg="#0b4f64", fg="white")
    if i == 0:
        label_numero.place(x=40, y=130)
    if i == 1:
        label_numero.place(x=40, y=180)
    if i == 2:
        label_numero.place(x=40, y=230)
    if i == 3:
        label_numero.place(x=40, y=280)

for i in range(1, 5):
    boton = tk.Button(ventana_secundaria, text=str(i), command=lambda i=i: seleccionar_respuesta(i), padx=10, pady=10, font=fontStyle)
    boton.config(bg="white", fg="black")
    if i == 1:
        boton.place(x=400, y=400, width=130, height=80)
    if i == 2:
        boton.place(x=750, y=400, width=130, height=80)
    if i == 3:
        boton.place(x=400, y=550, width=130, height=80)
    if i == 4:
        boton.place(x=750, y=550, width=130, height=80)

respuesta_seleccionada = None

ventana_logros = tk.Toplevel()
ancho_pantalla_logros = ventana_logros.winfo_screenwidth()
alto_pantalla_logros = ventana_logros.winfo_screenheight()
ventana_logros.geometry(f"{ancho_pantalla}x{alto_pantalla}")
ventana_logros.title("Logros")
ventana_logros.withdraw()

# Crear Treeview para mostrar la información
tree = ttk.Treeview(ventana_logros, columns=("Id","Nombre", "Instagram", "Puntaje", "Tiempo"))
tree.heading("#1", text="Id")
tree.heading("#2", text="Nombre")
tree.heading("#3", text="Instagram")
tree.heading("#4", text="Puntaje")
tree.heading("#5", text="Tiempo")

tree.column("#0", width=0, stretch=tk.NO)  # Ocultar la columna #0 que habitualmente muestra las primary key de los objetos

tree.pack(padx=10, pady=10)

Trofeo = tk.PhotoImage(file="Trofeo.png")
boton_trofeo = tk.Button(ventana, text="Trofeo", image=Trofeo, command=abrir_ventana_logros)
boton_trofeo.place(x=1000, y=460, width=75, height=50)
boton_trofeo.config(relief="sunken") 
ventana_logros.overrideredirect(True)
cargar_button = tk.Button(ventana_logros, text="Cargar Datos", font=fontStyle, command=cargar_usuario)
cargar_button.place(x=550, y=360, width=185, height=50)

boton_cerrar = tk.Button(
    ventana_logros,
    text="Cerrar ventana", 
    command=ventana_logros.withdraw,
    font=fontStyle)
boton_cerrar.place(x=1000, y=650)  

ventana.mainloop()

conexion.close()