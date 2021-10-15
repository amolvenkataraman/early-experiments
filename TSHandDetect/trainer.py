import cv2
import math
import mediapipe as mp
import pickle

from pynput.mouse import Button, Controller
mouse = Controller()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

LANDMARKS = []

# For webcam input:
cap = cv2.VideoCapture(1)
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
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                if results.multi_handedness[i].classification[0].label == "Right":
                    ee = list(hand_landmarks.landmark)
                    temp = {}
                    for j in range(0, 21):
                        temp[j] = [ee[j].x, ee[j].y, ee[j].z]
                    LANDMARKS.append(temp)
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

f = open('4.ct', 'wb')
pickle.dump(LANDMARKS, f)
f.close()
print(f"Saved {len(LANDMARKS)} snapshots to file")

cap.release()
