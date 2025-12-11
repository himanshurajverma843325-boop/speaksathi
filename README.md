# ✋ Gesture-to-Voice Translator | AI + Computer Vision

A real-time **hand gesture recognition** and **voice output system** built using  
**MediaPipe + OpenCV + Python + Text-to-Speech (pyttsx3)**.  

This project detects the number of fingers shown in front of the camera and speaks  
the corresponding voice command (e.g., “One”, “Two”, “Hello”, etc.).  
It can be extended to support custom gestures for accessibility, smart home control,  
robotics, and silent communication.

---

## 🚀 Features

- ✔️ Real-time hand detection using MediaPipe  
- ✔️ Detects finger counts (0–5) with high accuracy  
- ✔️ Converts gestures into **voice output**  
- ✔️ Fast and optimized — lower resolution processing for better FPS  
- ✔️ Works offline (no internet required)  
- ✔️ Easily extendable with custom gestures  

---

## 🎥 Demo Output (Sample)

| Gesture | System Says |
|--------|-------------|
| ✊ Fist | “Fist” |
| ☝️ One Finger | “One” |
| ✌️ Two Fingers | “Two” |
| 🤟 Three Fingers | “Three” |
| 🖐️ Five Fingers | “Hello” |

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV** → Camera capture & image processing  
- **MediaPipe Hands** → Gesture & landmark detection  
- **pyttsx3** → Offline Text-to-Speech voice output  
- **Threading** → Non-blocking voice playback  

---

## 📦 Installation

### 1️⃣ Clone this repository:
```bash
git clone https://github.com/YourUsername/Gesture-Voice-Translator.git
cd Gesture-Voice-Translator
