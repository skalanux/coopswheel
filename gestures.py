import cv2
import mediapipe as mp
import math

# Inicializamos mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Función para calcular la distancia euclidiana entre dos puntos
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def write_to_fifo(char):
    with open('gesture', 'w') as fifo:
        if char is not None:
            fifo.write(char)
            fifo.flush()  # Asegúrate de que los datos se escriban inmediatamente

# Función para clasificar el gesto
def classify_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    thumb_mcp = landmarks[2]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]

    # Calculamos la pendiente del pulgar
    thumb_slope = (thumb_tip.y - thumb_mcp.y) / (thumb_tip.x - thumb_mcp.x + 0.0001)

    # Clasificamos el gesto
    if thumb_tip.y < thumb_mcp.y and index_tip.y > index_mcp.y and middle_tip.y > middle_mcp.y and ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y:
        write_to_fifo("U")
        return "Pulgar arriba"
    elif thumb_tip.y > thumb_mcp.y and index_tip.y > index_mcp.y and middle_tip.y > middle_mcp.y and ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y:
        write_to_fifo("D")
        return "Pulgar abajo"
    elif thumb_tip.y < thumb_mcp.y and index_tip.y < index_mcp.y and middle_tip.y < middle_mcp.y and ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y:
        write_to_fifo("V")
        return "V de victoria"
    elif thumb_tip.y < thumb_mcp.y and index_tip.y < index_mcp.y and middle_tip.y < middle_mcp.y and ring_tip.y < ring_mcp.y and pinky_tip.y < pinky_mcp.y:
        write_to_fifo("O")
        return "Mano abierta"
    else:
        return ""

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertimos la imagen a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesamos la imagen con mediapipe
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtenemos la clasificación del gesto
            gesture = classify_gesture(hand_landmarks.landmark)
            cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('Detector de Gestos', frame)

    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

