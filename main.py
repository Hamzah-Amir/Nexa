from queue import Queue
import threading
from datetime import datetime
from tts import NexaSpeaker
from listener import NexaListener
from search_api import Nexa_search, NexaSearch

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
                    nexa_search = NexaSearch()
                    report = Nexa_search.search(command)
                    print("Report gathered: ", report['response'])
                    Nexa.speak(f"Nexa has gathered the report: {report['response']}")

                elif "what is time" in command:
                    now = datetime.now().strftime("%H:%M")
                    Nexa.speak(f"The current time is {now}.")
                    
                elif "exit" in command or "quit" in command:
                    Nexa.speak("Goodbye!")
                    break
        