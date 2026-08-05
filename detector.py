import cv2
import mediapipe as mp
import numpy as np
import teclado
import gestos

# =========================
# MEDIA PIPE
# =========================
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(1)

print("Iniciando software de asistencia... Presiona 'Esc' para cerrar.")

calibrado = False
key = 0
# =========================
# LOOP PRINCIPAL
# =========================
while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    # =========================
    # GESTOS
    # =========================

    boca_abierta = gestos.detectar_boca_abierta(results, frame)


    # =========================
    # DETECCIÓN DE CARA
    # =========================

    face_landmarks = None

    if results.multi_face_landmarks:

        face_landmarks = results.multi_face_landmarks[0]


    # =========================
    # CALIBRACIÓN
    # =========================

    if not calibrado:

        if face_landmarks is not None:

            if boca_abierta or key == 13:

                gestos.calibrar(face_landmarks)

                calibrado = True

                print("Calibracion completada")


    # =========================
    # MOVIMIENTOS DE CABEZA
    # =========================

    if calibrado and face_landmarks is not None:

        if gestos.cabeza_izquierda(face_landmarks) and gestos.delay(0.5):
            teclado.izquierda()

        elif gestos.cabeza_derecha(face_landmarks) and gestos.delay(0.5):
            teclado.derecha()

        elif gestos.cabeza_arriba(face_landmarks) and gestos.delay(0.5):
            teclado.arriba()

        elif gestos.cabeza_abajo(face_landmarks) and gestos.delay(0.5):
            teclado.abajo()

        if boca_abierta and gestos.delay_enter(0.5):
            teclado.enter()


    # =========================
    # TECLADO VISUAL
    # =========================

    img_teclado = teclado.dibujar()

    frame = cv2.resize(frame, (800, 800))

    combinada = np.hstack((frame, img_teclado))


    if not calibrado:

        cv2.putText(
            combinada,
            "Esperando calibracion...",
            (50, 750),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,255),
            2
        )


    cv2.imshow(
        'Asistente Biomedico - Juan Carlo',
        combinada
    )


    # =========================
    # TECLADO FISICO
    # =========================

    key = cv2.waitKey(1)


    if key == 27:
        break

    elif key == 32:
        teclado.espacio()

    elif key == 45:
        teclado.eliminar()

    elif key == 61:
        teclado.imprimir()


cap.release()
cv2.destroyAllWindows()