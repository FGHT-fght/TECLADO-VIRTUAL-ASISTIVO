import cv2
import mediapipe as mp

# =========================
# MEDIA PIPE
# =========================

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(1)

print("Iniciando prueba de iris... Presiona ESC para cerrar.")

# =========================
# LOOP PRINCIPAL
# =========================

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = face_mesh.process(rgb_frame)

    # =========================
    # DETECCIÓN DE CARA
    # =========================

    if results.multi_face_landmarks:

        face_landmarks = results.multi_face_landmarks[0]

        # Dibujar líneas del iris
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(0, 255, 0),
                thickness=1
            )
        )

        # =========================
        # CENTRO DEL IRIS
        # =========================

        iris = face_landmarks.landmark[468]

        h, w, _ = frame.shape

        iris_x = int(iris.x * w)
        iris_y = int(iris.y * h)

        cv2.circle(
            frame,
            (iris_x, iris_y),
            5,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            frame,
            f"Iris X: {iris.x:.3f} Y: {iris.y:.3f}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2
        )

    # =========================
    # MOSTRAR
    # =========================

    cv2.imshow(
        "Prueba Iris",
        frame
    )

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()