import cv2
import pickle
import numpy as np
import mediapipe as mp
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge


class FiltroDinamico:

    def __init__(self, radio_zona_muerta=20.0, alfa_minimo=0.08, alfa_maximo=0.85, umbral_velocidad=120.0):
        self.radio_zona_muerta = radio_zona_muerta
        self.alfa_minimo = alfa_minimo
        self.alfa_maximo = alfa_maximo
        self.umbral_velocidad = umbral_velocidad
        self.ultima_salida = None

    def actualizar(self, x_actual, y_actual):
        if self.ultima_salida is None:
            self.ultima_salida = np.array([x_actual, y_actual], dtype=float)
            return self.ultima_salida[0], self.ultima_salida[1]

        posicion_actual = np.array([x_actual, y_actual], dtype=float)
        distancia = np.linalg.norm(posicion_actual - self.ultima_salida)

        if distancia < self.radio_zona_muerta:
            return self.ultima_salida[0], self.ultima_salida[1]

        relacion_velocidad = min(distancia / self.umbral_velocidad, 1.0)
        alfa = self.alfa_minimo + (self.alfa_maximo - self.alfa_minimo) * relacion_velocidad

        posicion_filtrada = alfa * posicion_actual + (1 - alfa) * self.ultima_salida
        self.ultima_salida = posicion_filtrada

        return posicion_filtrada[0], posicion_filtrada[1]


class ClicPorPermanencia:

    def __init__(self, tiempo_permanencia_seg=2.5, radio_px=35.0, tiempo_espera_seg=1.0):
        self.tiempo_permanencia = tiempo_permanencia_seg
        self.radio = radio_px
        self.tiempo_espera_seg = tiempo_espera_seg

        self.posicion_ancla = None
        self.tiempo_inicio = None
        self.espera_hasta = 0.0

    def actualizar(self, x_actual, y_actual, marca_tiempo_actual):
        if marca_tiempo_actual < self.espera_hasta:
            return 0.0, False

        if self.posicion_ancla is None:
            self.posicion_ancla = (x_actual, y_actual)
            self.tiempo_inicio = marca_tiempo_actual
            return 0.0, False

        distancia = np.linalg.norm(np.array([x_actual, y_actual]) - np.array(self.posicion_ancla))

        if distancia > self.radio:
            self.posicion_ancla = (x_actual, y_actual)
            self.tiempo_inicio = marca_tiempo_actual
            return 0.0, False

        tiempo_transcurrido = marca_tiempo_actual - self.tiempo_inicio
        progreso = min(tiempo_transcurrido / self.tiempo_permanencia, 1.0)

        if progreso >= 1.0:
            self.posicion_ancla = (x_actual, y_actual)
            self.tiempo_inicio = marca_tiempo_actual
            self.espera_hasta = marca_tiempo_actual + self.tiempo_espera_seg
            return 1.0, True

        return progreso, False


class RastreadorOcularBase:

    def __init__(self):
        self.malla_facial = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.IRIS_IZQUIERDO_CENTRO = 468
        self.OJO_IZQUIERDO_ESQUINA_EXTERNA = 33
        self.OJO_IZQUIERDO_ESQUINA_INTERNA = 133

        self.modelo_x = None
        self.modelo_y = None
        self.transformador_polinomial = None
        self.desplazamiento_x = 0.0
        self.desplazamiento_y = 0.0

    def procesar_fotograma(self, fotograma):
        alto, ancho, _ = fotograma.shape
        fotograma_rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        resultados = self.malla_facial.process(fotograma_rgb)

        if not resultados.multi_face_landmarks:
            return None, None

        puntos_referencia = resultados.multi_face_landmarks[0].landmark

        iris = np.array([puntos_referencia[self.IRIS_IZQUIERDO_CENTRO].x * ancho, puntos_referencia[self.IRIS_IZQUIERDO_CENTRO].y * alto])
        esquina_externa = np.array(
            [puntos_referencia[self.OJO_IZQUIERDO_ESQUINA_EXTERNA].x * ancho, puntos_referencia[self.OJO_IZQUIERDO_ESQUINA_EXTERNA].y * alto])
        esquina_interna = np.array(
            [puntos_referencia[self.OJO_IZQUIERDO_ESQUINA_INTERNA].x * ancho, puntos_referencia[self.OJO_IZQUIERDO_ESQUINA_INTERNA].y * alto])

        ancho_ojo = np.linalg.norm(esquina_interna - esquina_externa)
        if ancho_ojo == 0:
            return None, None

        x_relativa = (iris[0] - esquina_externa[0]) / ancho_ojo
        y_relativa = (iris[1] - esquina_externa[1]) / ancho_ojo

        return x_relativa, y_relativa

    def predecir_punto_pantalla(self, x_relativa, y_relativa):
        if self.modelo_x is None or self.modelo_y is None or self.transformador_polinomial is None:
            raise ValueError("El modelo de calibración no ha sido cargado.")

        caracteristicas = self.transformador_polinomial.transform([[x_relativa, y_relativa]])
        pantalla_x = self.modelo_x.predict(caracteristicas)[0] + self.desplazamiento_x
        pantalla_y = self.modelo_y.predict(caracteristicas)[0] + self.desplazamiento_y
        return pantalla_x, pantalla_y

    def guardar_calibracion(self, ruta_archivo="calibracion_usuario.pkl"):
        datos = {
            "modelo_x": self.modelo_x,
            "modelo_y": self.modelo_y,
            "transformador_polinomial": self.transformador_polinomial
        }
        with open(ruta_archivo, "wb") as archivo:
            pickle.dump(datos, archivo)

    def cargar_calibracion(self, ruta_archivo="calibracion_usuario.pkl"):
        with open(ruta_archivo, "rb") as archivo:
            datos = pickle.load(archivo)
            self.modelo_x = datos["modelo_x"]
            self.modelo_y = datos["modelo_y"]
            self.transformador_polinomial = datos["transformador_polinomial"]