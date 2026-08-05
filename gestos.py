import cv2
import numpy as np
import time

# =========================
# CONFIGURACIÓN GENERAL
# =========================

umbral = 0.03  # sensibilidad del movimiento
face_ref = None  # referencia de cabeza (calibración)


# =========================
# UTILIDAD: CENTRO DE CARA
# =========================
# def obtener_centro(face_landmarks):
#     """
#     Calcula un punto estable del rostro usando varios landmarks
#     """

#     puntos = [1, 33, 263, 61, 291]  # nariz + pómulos + laterales

#     x, y = 0, 0

#     for i in puntos:
#         x += face_landmarks.landmark[i].x
#         y += face_landmarks.landmark[i].y

#     n = len(puntos)

#     return (x / n, y / n)
# =========================
# UTILIDAD: POSICIÓN DE NARIZ
# =========================
def obtener_centro(face_landmarks):
    """
    Usa solamente la nariz como referencia de movimiento
    """

    nariz = face_landmarks.landmark[1]

    return nariz.x, nariz.y

# =========================
# CALIBRACIÓN
# =========================
def calibrar(face_landmarks):
    global face_ref
    face_ref = obtener_centro(face_landmarks)


# =========================
# MOVIMIENTO DE CABEZA
# =========================
def cabeza_izquierda(face_landmarks):
    global face_ref

    x, y = obtener_centro(face_landmarks)

    if face_ref is None:
        face_ref = (x, y)
        return False

    dx = x - face_ref[0]

    return dx < -umbral


def cabeza_derecha(face_landmarks):
    global face_ref

    x, y = obtener_centro(face_landmarks)

    if face_ref is None:
        face_ref = (x, y)
        return False

    dx = x - face_ref[0]

    return dx > umbral


def cabeza_arriba(face_landmarks):
    global face_ref

    x, y = obtener_centro(face_landmarks)

    if face_ref is None:
        face_ref = (x, y)
        return False

    dy = y - face_ref[1]

    return dy < -umbral


def cabeza_abajo(face_landmarks):
    global face_ref

    x, y = obtener_centro(face_landmarks)

    if face_ref is None:
        face_ref = (x, y)
        return False

    dy = y - face_ref[1]
    
    return dy > umbral


# =========================
# DETECCIÓN BOCA ABIERTA
# =========================
def detectar_boca_abierta(results, frame):

    boca_abierta = False

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            p13 = face_landmarks.landmark[13]
            p14 = face_landmarks.landmark[14]

            distancia = abs(p13.y - p14.y)

            if distancia > 0.04:

                boca_abierta = True

                cv2.putText(
                    frame,
                    "Gesto: BOCA ABIERTA",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "Gesto: BOCA CERRADA",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

    return boca_abierta

# =========================
# DELAY PARA EVITAR FALSOS POSITIVOS
# =========================
ultima_lectura = time.time()
ultima_lectura_enter = time.time()

def delay(segundos):
    global ultima_lectura

    lectura_actual = time.time()

    if lectura_actual - ultima_lectura >= segundos:
        ultima_lectura = lectura_actual #importante sino se quedara atrapado con siempre positivo
        return True

    return False

def delay_enter(segundos): 
    global ultima_lectura_enter

    lectura_actual = time.time()

    if lectura_actual - ultima_lectura_enter >= segundos:
        ultima_lectura_enter = lectura_actual
        return True

    return False
