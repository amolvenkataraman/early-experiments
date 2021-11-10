import cv2
import math
import mediapipe as mp
import tensorflow as tf

from pynput.mouse import Button, Controller
mouse = Controller()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

model = tf.keras.models.load_model('model.h5')

GESTURES = ["Flat Palm", "Thumps Up", "Thumbs Down", "One", "Two"]

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for handno, hand_landmarks in enumerate(results.multi_hand_landmarks):
                temp = []
                for i in range(21):
                    temp.append(hand_landmarks.landmark[i].x)
                    temp.append(hand_landmarks.landmark[i].y)
                    temp.append(hand_landmarks.landmark[i].z)

                ans = list(model.predict([temp])[0])
                #print(GESTURES[ans.index(max(ans))])
                image = cv2.putText(image, GESTURES[ans.index(max(ans))], (50, 50 * (handno + 1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

                mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
