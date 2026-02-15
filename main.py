from queue import Queue
import threading
from datetime import datetime
from tts import NexaSpeaker
from listener import NexaListener
from search_api import NexaSearch

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
                elif "search" in command.lower() or "what is" in command.lower():
                    Nexa.speak("Nexa is searching, give her a minute.")
                    report = NexaSearch.search(command)
                    Nexa.speak(f"Nexa has gathered the report: {report}")
                elif "what is time" in command:
                    now = datetime.now().strftime("%H:%M")
                    Nexa.speak(f"The current time is {now}.")
                elif "exit" in command or "quit" in command:
                    Nexa.speak("Goodbye!")
                    break
        