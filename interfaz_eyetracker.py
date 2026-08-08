import tkinter as tk

# =========================
# CONFIGURACIÓN INICIAL
# =========================
ventana = tk.Tk()

ventana.title("Eye Tracker")
ventana.geometry("1280x720")
ventana.configure(bg="black")

# =========================
# VARIABLES DEL MENU
# =========================
opciones = [
    "INICIAR",
    "CONFIGURACIÓN",
    "SALIR"
]

opciones_confirmacion = [
    "SI",
    "NO"
]

opciones_inicio = [
    "NUEVA CALIBRACIÓN",
    "CARGAR CALIBRACIÓN",
    "BORRAR CALIBRACIÓN"
]

opciones_nueva_calibracion = [
    "INICIO",
    "ATRÁS"
]

seleccion = 0
estado_menu = "principal"

# =========================
# FUNCIONES
# =========================
def actualizar_menu():
    global estado_menu

    if estado_menu == "principal":
        opciones_actuales = opciones
        pregunta.config(text="")
        subtitulo.pack()
        advertencia.config(text="")
        advertencia.pack_forget()
    elif estado_menu == "confirmacion":
        opciones_actuales = opciones_confirmacion
        pregunta.config(text="¿ESTÁS SEGURO QUE QUIERES CERRAR EL PROGRAMA?")
        subtitulo.pack_forget()
        advertencia.config(text="")
        advertencia.pack_forget()
    elif estado_menu == "nueva_calibracion":
        opciones_actuales = opciones_nueva_calibracion
        pregunta.config(text="PRESIONE INICIO PARA EMPEZAR")
        subtitulo.pack_forget()
        advertencia.config(text="AJUSTAR EL TAMAÑO DE LA VENTANA A PANTALLA COMPLETA")
        advertencia.pack()
    else:
        opciones_actuales = opciones_inicio
        pregunta.config(text="SELECCIONA UNA OPCIÓN")
        subtitulo.pack_forget()
        advertencia.config(text="")
        advertencia.pack_forget()

    texto = ""

    for i, opcion in enumerate(opciones_actuales):
        if i == seleccion:
            texto += f"▶ {opcion}\n\n"
        else:
            texto += f"{opcion}\n\n"

    menu.config(text=texto)

def mover_arriba(event):
    global seleccion

    seleccion -= 1

    if estado_menu == "principal":
        if seleccion < 0:
            seleccion = len(opciones) - 1
    elif estado_menu == "confirmacion":
        if seleccion < 0:
            seleccion = len(opciones_confirmacion) - 1
    elif estado_menu == "nueva_calibracion":
        if seleccion < 0:
            seleccion = len(opciones_nueva_calibracion) - 1
    else:
        if seleccion < 0:
            seleccion = len(opciones_inicio) - 1

    actualizar_menu()

def mover_abajo(event):
    global seleccion

    seleccion += 1

    if estado_menu == "principal":
        if seleccion >= len(opciones):
            seleccion = 0
    elif estado_menu == "confirmacion":
        if seleccion >= len(opciones_confirmacion):
            seleccion = 0
    elif estado_menu == "nueva_calibracion":
        if seleccion >= len(opciones_nueva_calibracion):
            seleccion = 0
    else:
        if seleccion >= len(opciones_inicio):
            seleccion = 0

    actualizar_menu()

def seleccionar(event):
    global seleccion, estado_menu

    if estado_menu == "principal":
        opcion = opciones[seleccion]

        if opcion == "INICIAR":
            estado_menu = "inicio"
            seleccion = 0
            actualizar_menu()
        elif opcion == "SALIR":
            estado_menu = "confirmacion"
            seleccion = 0
            actualizar_menu()
        else:
            print("Seleccionado:", opcion)
    elif estado_menu == "confirmacion":
        opcion = opciones_confirmacion[seleccion]

        if opcion == "SI":
            ventana.destroy()
        else:
            estado_menu = "principal"
            seleccion = 2
            actualizar_menu()
    elif estado_menu == "nueva_calibracion":
        opcion = opciones_nueva_calibracion[seleccion]
        print("Seleccionado:", opcion)

        if opcion == "INICIO":
            print("Iniciando calibración...")
        else:
            estado_menu = "inicio"
            seleccion = 0
            actualizar_menu()
    else:
        opcion = opciones_inicio[seleccion]
        print("Seleccionado:", opcion)

        if opcion == "NUEVA CALIBRACIÓN":
            estado_menu = "nueva_calibracion"
            seleccion = 0
            actualizar_menu()
        else:
            estado_menu = "principal"
            seleccion = 0
            actualizar_menu()


def volver_atras(event):
    global seleccion, estado_menu

    if estado_menu == "confirmacion":
        estado_menu = "principal"
        seleccion = 2
        actualizar_menu()
    elif estado_menu == "nueva_calibracion":
        estado_menu = "inicio"
        seleccion = 0
        actualizar_menu()
    elif estado_menu == "inicio":
        estado_menu = "principal"
        seleccion = 0
        actualizar_menu()
    else:
        estado_menu = "confirmacion"
        seleccion = 0
        actualizar_menu()

# =========================
# TITULO
# =========================
titulo = tk.Label(
    ventana,
    text="EYE TRACKER",
    font=("Impact", 42, "bold"),
    fg="white",
    bg="black"
)

titulo.pack(pady=80)

# =========================
# SUBTITULO
# =========================
subtitulo = tk.Label(
    ventana,
    text="Sistema de control ocular",
    font=("Impact", 18),
    fg="white",
    bg="black"
)

subtitulo.pack()

# =========================
# MENU
# =========================
pregunta = tk.Label(
    ventana,
    text="",
    font=("Impact", 18),
    fg="white",
    bg="black"
)

pregunta.pack(pady=(0, 10))

advertencia = tk.Label(
    ventana,
    text="",
    font=("Impact", 14),
    fg="yellow",
    bg="black"
)

advertencia.pack(pady=(0, 8))

menu = tk.Label(
    ventana,
    text="",
    font=("Impact", 24),
    fg="white",
    bg="black",
    justify="center",
    width=24,
    anchor="center"
)

menu.pack(expand=True)

actualizar_menu()

# =========================
# VERSION
# =========================
version = tk.Label(
    ventana,
    text="Version 0.1",
    font=("Impact", 12),
    fg="gray",
    bg="black"
)

version.pack(side="bottom", pady=20)

# =========================
# CONTROLES
# =========================
ventana.bind("<Up>", mover_arriba)
ventana.bind("<Down>", mover_abajo)
ventana.bind("<Return>", seleccionar)
ventana.bind("<Escape>", volver_atras)

# =========================
# INICIO
# =========================
ventana.mainloop()