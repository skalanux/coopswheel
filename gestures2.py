import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# STEP 1: Create an GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

# STEP 2: Initialize the camera
cap = cv2.VideoCapture(0)  # 0 for default camera

def write_to_fifo(char):
    with open('gesture', 'w') as fifo:
        if char is not None:
            fifo.write(char)
            fifo.flush()  # Asegúrate de que los datos se escriban inmediatamente


while True:
    # STEP 3: Read frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # STEP 4: Convert the frame to RGB (MediaPipe uses RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    # STEP 5: Recognize gestures in the input image
    recognition_result = recognizer.recognize(mp_image)

    # STEP 6: Process the result
    if recognition_result.gestures:
        top_gesture = recognition_result.gestures[0][0]
        gesture = ''

        match top_gesture.category_name:
            case "Victory":
                gesture = 'V'
            case "Thumb_Up":
                gesture = 'U'
            case "Thumb_Down":
                gesture = 'D'
            case "Open_Palm":
                gesture = 'O'
            case "Closed_Fist":
                gesture = 'X'
            case default:
                gesture = '-'
        write_to_fifo(gesture)
        # Draw hand landmarks
        if recognition_result.hand_landmarks:
            for hand_landmarks in recognition_result.hand_landmarks:
                for landmark in hand_landmarks:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # STEP 7: Display the frame
    cv2.imshow('Gesture Recognition', frame)

    # STEP 8: Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# STEP 9: Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
