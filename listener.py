import speech_recognition as sr

class NexaListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.energy_threshold = 300
            self.recognizer.pause_threshold = 0.7
    
    def listen(self):
        with self.microphone as source:
            print("Nexa Listening...")
            audio = self.recognizer.listen(source)
        try:
            command = self.recognizer.recognize_google(audio)
            if command.startswith("Nexa") or command.startswith("nexa"):
                print(f"Nexa Heard: {command}")
                return command.lower()
        except sr.UnknownValueError:
            print("Nexa could not understand the audio.")
            return None
