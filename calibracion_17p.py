import cv2
import time
import pyautogui
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from eye_tracker import RastreadorOcularBase

pyautogui.FAILSAFE = False


def obtener_17_puntos(ancho_pantalla, alto_pantalla):
    lista_x = [int(ancho_pantalla * factor) for factor in [0.1, 0.3, 0.5, 0.7, 0.9]]
    lista_y = [int(alto_pantalla * factor) for factor in [0.1, 0.3, 0.5, 0.7, 0.9]]

    puntos = [
        (lista_x[2], lista_y[2]), (lista_x[0], lista_y[0]), (lista_x[4], lista_y[0]), (lista_x[0], lista_y[4]), (lista_x[4], lista_y[4]),
        (lista_x[2], lista_y[0]), (lista_x[2], lista_y[4]), (lista_x[0], lista_y[2]), (lista_x[4], lista_y[2]),
        (lista_x[1], lista_y[1]), (lista_x[3], lista_y[1]), (lista_x[1], lista_y[3]), (lista_x[3], lista_y[3]),
        (lista_x[1], lista_y[2]), (lista_x[3], lista_y[2]), (lista_x[2], lista_y[1]), (lista_x[2], lista_y[3])
    ]
    return puntos


def ejecutar_calibracion_17_puntos():
    rastreador = RastreadorOcularBase()
    captura = cv2.VideoCapture(0)

    nombre_ventana = "Calibracion 17 Puntos"
    cv2.namedWindow(nombre_ventana, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(nombre_ventana, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    ancho_pantalla, alto_pantalla = pyautogui.size()
    puntos = obtener_17_puntos(ancho_pantalla, alto_pantalla)

    entrada_ojo, salida_pantalla = [], []
    TIEMPO_PREPARACION, TIEMPO_CAPTURA = 1.2, 1.5

    for indice_punto, (punto_x, punto_y) in enumerate(puntos):
        tiempo_inicio = time.time()
        muestras = []

        while True:
            exito, fotograma = captura.read()
            if not exito:
                break
            fotograma = cv2.flip(fotograma, 1)
            x_relativa, y_relativa = rastreador.procesar_fotograma(fotograma)

            tiempo_transcurrido = time.time() - tiempo_inicio
            lienzo = np.zeros((alto_pantalla, ancho_pantalla, 3), dtype=np.uint8)

            if tiempo_transcurrido < TIEMPO_PREPARACION:
                cv2.drawMarker(lienzo, (punto_x, punto_y), (0, 0, 255), cv2.MARKER_CROSS, 40, 3)
                cv2.putText(lienzo, f"Mire el punto ({indice_punto + 1}/17)", (punto_x - 80, punto_y - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            elif tiempo_transcurrido < (TIEMPO_PREPARACION + TIEMPO_CAPTURA):
                cv2.drawMarker(lienzo, (punto_x, punto_y), (0, 255, 0), cv2.MARKER_CROSS, 40, 3)
                if x_relativa is not None and y_relativa is not None:
                    muestras.append([x_relativa, y_relativa])
            else:
                break

            cv2.imshow(nombre_ventana, lienzo)
            if cv2.waitKey(1) & 0xFF == 27:
                captura.release()
                cv2.destroyAllWindows()
                return

        if muestras:
            promedio_ojo = np.mean(muestras, axis=0)
            entrada_ojo.append(promedio_ojo)
            salida_pantalla.append([punto_x, punto_y])

    captura.release()
    cv2.destroyAllWindows()

    entrada_ojo = np.array(entrada_ojo)
    salida_pantalla = np.array(salida_pantalla)

    polinomio = PolynomialFeatures(degree=2)
    entrada_polinomial = polinomio.fit_transform(entrada_ojo)

    modelo_x = Ridge(alpha=1.0).fit(entrada_polinomial, salida_pantalla[:, 0])
    modelo_y = Ridge(alpha=1.0).fit(entrada_polinomial, salida_pantalla[:, 1])

    rastreador.transformador_polinomial = polinomio
    rastreador.modelo_x = modelo_x
    rastreador.modelo_y = modelo_y
    rastreador.guardar_calibracion("calibracion_usuario.pkl")
    print("Calibración guardada")


if __name__ == "__main__":
    ejecutar_calibracion_17_puntos()