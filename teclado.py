# teclado.py

import cv2
import numpy as np
# =========================
# VARIABLES
# =========================
img = np.zeros((800, 900, 3), dtype=np.uint8)

texto = ""

teclado = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ñ"],
    ["Z", "X", "C", "V", "B", "N", "M", " ", "-"]
]

sel_i = 0
sel_j = 0

ancho = 80
alto = 80

x_inicio = 50
y_inicio = 100
# =========================
# MOVIMIENTO
# =========================
def izquierda():
    global sel_j
    if sel_j > 0:
        sel_j -= 1

def derecha():
    global sel_j
    if sel_j < len(teclado[sel_i]) - 1:
        sel_j += 1

def arriba():
    global sel_i
    global sel_j
    if sel_i > 0:
        sel_i -= 1
        sel_j = min(sel_j, len(teclado[sel_i]) - 1)

def abajo():
    global sel_i
    global sel_j
    if sel_i < len(teclado) - 1:
        sel_i += 1
        sel_j = min(sel_j, len(teclado[sel_i]) - 1)
# =========================
# TEXTO
# =========================
def enter():
    global texto
    letra = teclado[sel_i][sel_j]
    if letra == "-":
        texto = ""
        return
    
    texto += letra

def espacio():
    global texto
    texto += " "

def eliminar():
    global texto
    texto = texto[:-1]

def imprimir():
    print(texto)

def obtener_texto():
    return texto

def limpiar_texto():
    global texto
    texto = ""
# =========================
# PANTALLA
# =========================
def dibujar():
    global img
    # limpiar pantalla
    img[:] = 0
    # mostrar texto escrito
    cv2.putText(
        img,
        texto,
        (50, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (255, 255, 255),
        2
    )

    # dibujar teclado
    for i, fila in enumerate(teclado):
        for j, tecla in enumerate(fila):
            x = x_inicio + j * ancho
            y = y_inicio + i * alto
            # tecla seleccionada
            if i == sel_i and j == sel_j:
                color = (0, 0, 255)
                thickness = 6
            else:
                color = (0, 255, 0)
                thickness = 2
            cv2.rectangle(
                img,
                (x, y),
                (x + ancho, y + alto),
                color,
                thickness
            )
            cv2.putText(
                img,
                tecla,
                (x + 25, y + 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )
    return img
# =========================
# CERRAR
# =========================
def salir():
    cv2.destroyAllWindows()