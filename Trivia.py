import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont

# Preguntas y respuestas
preguntas_respuestas = [
    {
        "pregunta": "¿Cuál es la capital de Francia?",
        "opciones": ["Madrid", "Londres", "París", "Berlín"],
        "respuesta_correcta": "París"
    },
    {
        "pregunta": "¿Cuál es el río más largo del mundo?",
        "opciones": ["Nilo", "Amazonas", "Mississippi", "Yangtsé"],
        "respuesta_correcta": "Amazonas"
    },
    {
        "pregunta": "¿Cuál es el planeta más grande del sistema solar?",
        "opciones": ["Tierra", "Marte", "Júpiter", "Venus"],
        "respuesta_correcta": "Júpiter"
    }
]

# Variables globales
indice_pregunta_actual = 0
respuestas_correctas = 0

def abrir_ventana_secundaria():
    ventana_secundaria.deiconify()  # Mostrar la ventana secundaria

def verificar_respuesta():
    global indice_pregunta_actual, respuestas_correctas
    respuesta_seleccionada = var.get()
    respuesta_correcta = preguntas_respuestas[indice_pregunta_actual]["respuesta_correcta"]
    
    if respuesta_seleccionada == respuesta_correcta:
        respuestas_correctas += 1
    
    indice_pregunta_actual += 1
    
    if indice_pregunta_actual < len(preguntas_respuestas):
        mostrar_pregunta()
    else:
        messagebox.showinfo("Fin del juego", f"Tu puntaje final es: {respuestas_correctas}/{len(preguntas_respuestas)}")
        ventana_secundaria.quit()

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
ventana.geometry("800x600")
ventana.title("Trivia Game")
fontStyle = tkFont.Font(family="Lucida Grande", size=20)

# Agregar la imagen a la ventana principal
image = tk.PhotoImage(file="ISAUILogo.png")
label_Imag = ttk.Label(ventana, image=image)
label_Imag.pack(side=tk.TOP)

jugar_boton = tk.Button(ventana, text="Jugar", command=abrir_ventana_secundaria, padx=10, pady=15, font=fontStyle)
jugar_boton.place(relx=0.5,rely=0.5,width=100,anchor='c')

# Crear una ventana secundaria.
ventana_secundaria = tk.Toplevel()
ventana_secundaria.title("Juego")
ventana_secundaria.geometry("800x600")
ventana_secundaria.withdraw()  # Ocultar la ventana secundaria inicialmente

boton_cerrar = ttk.Button(
    ventana_secundaria,
    text="Cerrar ventana", 
    command=ventana_secundaria.destroy)
boton_cerrar.place(x=600, y=550)    

# Etiqueta de la pregunta
pregunta_label = tk.Label(ventana_secundaria, text="", padx=10, pady=40, font=fontStyle)
pregunta_label.pack()

# Variables para almacenar la respuesta seleccionada
var = tk.StringVar()

# Variables de control para los botones de radio
var_opciones = [tk.StringVar() for _ in range(4)]

# Radio botones para las opciones de respuesta
radio_botones = []
for i in range(4):
    radio_boton = tk.Radiobutton(ventana_secundaria, text="", variable=var, value="", padx=10, pady=5, font=fontStyle)
    radio_boton.pack()
    radio_botones.append(radio_boton)

# Etiqueta para mostrar el puntaje
puntaje_label = tk.Label(ventana_secundaria, text="Respuestas correctas: 0/0", padx=10, pady=25, font=fontStyle)
puntaje_label.pack()

# Botón para verificar respuesta
verificar_boton = tk.Button(ventana_secundaria, text="Verificar respuesta", command=verificar_respuesta, padx=10, pady=15, font=fontStyle)
verificar_boton.pack()

# Iniciar el juego
mostrar_pregunta()

ventana.mainloop()
