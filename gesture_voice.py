import cv2
import mediapipe as mp
import pyttsx3
import threading
import time

# ---------------- Voice setup ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    """Non-blocking voice"""
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

# ---------------- Mediapipe hands ----------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ---------------- Camera ----------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)   # CAP_DSHOW for Windows camera fix
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_spoken_time = 0
cooldown = 0.5  # sec cooldown for stable voice

def count_fingers(hand_landmarks, hand_label):
    fingers = []

    # Thumb
    if hand_label == "Right":
        fingers.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else 0)

    # Other fingers
    finger_tips = [8, 12, 16, 20]
    finger_pip = [6, 10, 14, 18]
    for tip, pip in zip(finger_tips, finger_pip):
        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y else 0)

    return fingers.count(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not detected!")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    gesture = None

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            hand_label = hand_handedness.classification[0].label
            finger_count = count_fingers(hand_landmarks, hand_label)

            gesture_dict = {
                0: "Fist",
                1: "One",
                2: "Two",
                3: "Three",
                4: "Four",
                5: "Hello"
            }
            gesture = gesture_dict.get(finger_count, "")

    # ---------------- Voice ----------------
    if gesture:
        current_time = time.time()
        if current_time - last_spoken_time > cooldown:
            print("Speaking:", gesture)
            speak(gesture)
            last_spoken_time = current_time

    # ---------------- Display ----------------
    cv2.putText(frame, f'Gesture: {gesture if gesture else "None"}',
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    if gesture:
        cv2.rectangle(frame, (10, 70), (220, 120), (0, 255, 0), -1)
        cv2.putText(frame, gesture, (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Hand Gesture Voice", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
