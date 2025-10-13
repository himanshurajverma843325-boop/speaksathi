import pyttsx3

engine = pyttsx3.init('sapi5')  # Windows TTS
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.say("Hello, this is a speaksathi")
engine.runAndWait()
