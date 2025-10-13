import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Fingertip landmark indexes
finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                h, w, c = frame.shape
                landmarks = hand_landmarks.landmark

                finger_states = []

                # Thumb (x check, because thumb moves sideways)
                if landmarks[finger_tips[0]].x < landmarks[finger_tips[0] - 1].x:
                    finger_states.append(1)  # Open
                else:
                    finger_states.append(0)  # Closed

                # Other fingers (y check, fingertip higher than knuckle = open)
                for i in range(1, 5):
                    if landmarks[finger_tips[i]].y < landmarks[finger_tips[i] - 2].y:
                        finger_states.append(1)  # Open
                    else:
                        finger_states.append(0)  # Closed

                # Show result on screen
                cv2.putText(frame, f"Fingers: {finger_states}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Finger Open/Close Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
