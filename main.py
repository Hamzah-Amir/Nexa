from queue import Queue
import threading
from commands import commands
from datetime import datetime
from tts import NexaSpeaker
from listener import NexaListener
from search_api import NexaSearch
from utils import Utils

def listener_thread(listener, command_queue):
    while True:
        command = listener.listen()
        if command:
            command_queue.put(command)


if __name__ == "__main__":
    utils = Utils()
    Nexa = NexaSpeaker()
    nexa_search = NexaSearch()
    Nexa.speak("Nexa Standby, waiting for your command.")

    listener = NexaListener()
    command_queue = Queue()

    t = threading.Thread(target=listener_thread, args=(listener, command_queue), daemon=True)
    t.start()
    is_running = False
    while True:
            command = command_queue.get()
            command = command.lower()

            if not is_running:
                if "hello nexa" in command:
                    is_running = True
                    Nexa.speak("Initializing Nexa. How can I assist you?")
                continue

            if command in commands:
                commands[command]()
                if "hello" in command:
                    Nexa.speak("Hello! How can I assist you today?")

                elif "search" in command.lower() or "what is" in command.lower():
                    Nexa.speak("Nexa is searching, give her a minute.")
                    report = nexa_search.search(command)
                    print("Report gathered: ", report['response'])
                    Nexa.speak(f"Nexa has gathered the report: {report['response']}")

                elif "what is time" in command:
                    now = datetime.now().strftime("%H:%M")
                    Nexa.speak(f"The current time is {now}.")
                
                elif "generate image" in command.lower():
                    Nexa.speak("Nexa is generating the image, give her a minute.")
                    image_response = nexa_search.generate_image(command)
                    print("Image generated: ", image_response['image'])
                    Nexa.speak("Nexa has generated the image based on your query.")
                
                elif "open code" in command:
                    Nexa.speak("Opening Visual Studio Code for you.")
                    utils.open_code()
                
                elif "open browser" in command:
                    Nexa.speak("Opening your default web browser.")
                    utils.open_browser()
                
                elif "open linkedin" in command:
                    Nexa.speak("Opening LinkedIn for you.")
                    utils.open_linkedin()
                    
                elif "open facebook" in command:
                    Nexa.speak("Opening Facebook for you.")
                    utils.open_facebook()
                
                elif "open github" in command:
                    Nexa.speak("Opening GitHub for you.")
                    utils.open_github()
                
                elif "take screenshot" in command:
                    Nexa.speak("Taking a screenshot for you.")
                    screenshot_path = utils.take_screenshot()
                    Nexa.speak(f"Screenshot taken and saved as {screenshot_path}.")
                
                elif "copy" in command:
                    text_to_copy = command.replace("copy", "").strip()
                    utils.copy_to_clipboard(text_to_copy)
                    Nexa.speak("Text copied to clipboard.")
                
                elif "paste" in command:
                    clipboard_content = utils.read_from_clipboard()
                    Nexa.speak(f"The clipboard contains: {clipboard_content}")
                
                elif "lock screen" in command:
                    Nexa.speak("Locking your screen.")
                    utils.lock_screen()
                
                elif "type" in command:
                    text_to_type = command.replace("type", "").strip()
                    utils.type_text(text_to_type)
                    Nexa.speak("Typing the text for you.")
                
                elif "scroll up" in command:
                    utils.scroll_up()
                    Nexa.speak("Scrolled up.")
                
                elif "scroll down" in command:
                    utils.scroll_down()
                    Nexa.speak("Scrolled down.")
                
                elif "switch app" in command:
                    utils.switch_window()
                    Nexa.speak("Switched to the next app.")

                elif "exit" in command or "quit" in command:
                    Nexa.speak("Goodbye!")
                    is_running = False
        