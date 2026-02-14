from tts import NexaSpeaker
from listener import NexaListener
from queue import Queue
import threading
from datetime import datetime

def listener_thread(listener, command_queue):
    while True:
        command = listener.listen()
        if command:
            command_queue.put(command)

if __name__ == "__main__":
    Nexa = NexaSpeaker()
    Nexa.speak("Initializing Nexa...")
    
    listener = NexaListener()
    command_queue = Queue()

    t = threading.Thread(target=listener_thread, args=(listener, command_queue))
    t.start()

    while True:
        if not command_queue.empty():
            command = command_queue.get()
            if command:
                if "hello" in command:
                    Nexa.speak("Hello! How can I assist you today?")
                elif "what is time" in command:
                    now = datetime.now().strftime("%H:%M")
                    Nexa.speak(f"The current time is {now}.")
                elif "exit" in command or "quit" in command:
                    Nexa.speak("Goodbye!")
                    break
        