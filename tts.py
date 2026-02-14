import pyttsx3

class NexaSpeaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

    def speak(self, text):
        self.engine.setProperty('voice', 'english+f3')
        self.engine.say(text)
        self.engine.runAndWait()