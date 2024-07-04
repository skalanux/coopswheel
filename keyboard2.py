import cv2
import numpy as np
import mediapipe as mp
import time
import pyautogui

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Dimensiones de la ventana
width, height = 800, 800
key_size = 50

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
blue = (255, 0, 0)

# Inicializar la ventana
window = np.zeros((height, width, 3), np.uint8)
window[:] = white

# Definir las teclas y sus posiciones
keys = [
    ('Q', (50, 450)), ('W', (110, 250)), ('E', (170, 450)), ('R', (230, 450)), ('T', (290, 450)),
    ('Y', (350, 450)), ('U', (410, 450)), ('I', (470, 450)), ('O', (530, 450)), ('P', (590, 450)),
    ('A', (80, 510)), ('S', (140, 510)), ('D', (200, 510)), ('F', (260, 510)), ('G', (320, 510)),
    ('H', (380, 510)), ('J', (440, 510)), ('K', (500, 510)), ('L', (560, 510)),
    ('Z', (110, 570)), ('X', (170, 570)), ('C', (230, 570)), ('V', (290, 570)), ('B', (350, 570)),
    ('N', (410, 570)), ('M', (470, 570)), (' ', (290, 630))  # Tecla de espacio
]

# Función para dibujar las teclas
def draw_keys(img):
    for key, pos in keys:
        x, y = pos
        cv2.rectangle(img, (x, y), (x + key_size, y + key_size), black, 2)
        cv2.putText(img, key, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, black, 2)

# Función para encontrar si la punta del dedo está sobre una tecla
def get_key_under_finger(finger_pos):
    fx, fy = finger_pos
    for key, pos in keys:
        x, y = pos
        if x <= fx <= x + key_size and y <= fy <= y + key_size:
            return key, pos
    return None, None

# Captura de video
cap = cv2.VideoCapture(2)

# Tiempo de inicio para detectar si se ha detenido
start_time = None
selected_key = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Invertir la imagen horizontalmente para que sea un espejo
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen para encontrar las manos
    result = hands.process(frame_rgb)

    # Dibujar las teclas en el frame
    draw_keys(frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = frame.shape
            finger_x, finger_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Dibujar un círculo en la punta del dedo índice
            cv2.circle(frame, (finger_x, finger_y), 10, blue, cv2.FILLED)

            # Mover el cursor del ratón a la posición de la punta del dedo índice
            pyautogui.moveTo(finger_x, finger_y)

            # Comprobar si el dedo está sobre una tecla
            key, pos = get_key_under_finger((finger_x, finger_y))
            if key:
                if selected_key != key:
                    selected_key = key
                    start_time = time.time()
                elif time.time() - start_time > 1:  # 1 segundo de detención
                    print(f"Clicked on key: {key}")
                    pyautogui.click()
                    selected_key = None
                    start_time = None
            else:
                selected_key = None
                start_time = None

    # Mostrar el frame
    cv2.imshow('Virtual Keyboard', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Presiona 'ESC' para salir
        break

cap.release()
cv2.destroyAllWindows()

