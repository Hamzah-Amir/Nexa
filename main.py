from queue import Queue
import threading
from commands import commands
from datetime import datetime
from tts import NexaSpeaker
from listener import NexaListener
from search_api import NexaSearch
from utils import Utils
from logger import Logger
from random import choice

logger = Logger()

def listener_thread(listener, command_queue):
    while True:
        command = listener.listen()
        if command:
            command_queue.put(command)


starter_lines = [
        "Initializing Nexa. Ready to assist you.",
        "Hello! Nexa is up and running. How can I assist you today?",
        "Hello! Nexa online and listening.",
        "Nexa is ready to assist you. What can I do for you today?"
    ]


sleep_lines = [
        "Nexa is going to sleep. Say 'Nexa wake up' to wake me.",
        "Entering sleep mode. I'll be quiet until you call me.",
        "Nexa is taking a nap. I'll be here when you wake me up.",
        ]

wake_lines = [
        "Nexa is awake and ready to assist you.",
        "Back online! What can I do for you?",
        "Nexa is awake and listening. How can I help you?"
        "Nexa is back and ready to assist. What do you need?"
    ]

if __name__ == "__main__":
    utils = Utils()
    Nexa = NexaSpeaker()
    nexa_search = NexaSearch()
    is_awake = True
    Nexa.speak(choice(starter_lines))

    listener = NexaListener()
    command_queue = Queue()


    t = threading.Thread(target=listener_thread, args=(listener, command_queue), daemon=True)
    t.start()
    while True:
            command = command_queue.get()
            command = command.lower()

            if not is_awake and ("wake up" not in command):
                continue

            if command and is_awake:
                if "go to sleep" in command:
                    Nexa.speak(choice(sleep_lines))
                    is_awake = False
                    logger.log(command, "go_to_sleep", "Nexa went to sleep successfully.")

                elif "wake up" in command:
                    Nexa.speak(choice(wake_lines))
                    is_awake = True
                    logger.log(command, "wake_up", "Nexa woke up successfully.")

                elif "search" in command.lower() or "what is" in command.lower():
                    Nexa.speak("Nexa is searching, give her a minute.")
                    report = nexa_search.search(command)
                    print("Report gathered: ", report['response'])
                    Nexa.speak(f"Nexa has gathered the report: {report['response']}")
                    logger.log(command, "search", report['response'])

                elif "what is time" in command:
                    now = datetime.now().strftime("%H:%M")
                    Nexa.speak(f"The current time is {now}.")
                    logger.log(command, "time", now)
                
                elif "generate image" in command.lower():
                    Nexa.speak("Nexa is generating the image, give her a minute.")
                    image_response = nexa_search.generate_image(command)
                    print("Image generated: ", image_response['image'])
                    Nexa.speak("Nexa has generated the image based on your query.")
                    logger.log(command, "generate_image", f"Image generated successfully at {image_response['image']}")
                
                elif "open code" in command:
                    Nexa.speak("Opening Visual Studio Code for you.")
                    utils.open_code()
                    logger.log(command, "open_code", "Visual Studio Code opened successfully.")
                
                elif "open gmail" in command:
                    Nexa.speak("Opening Gmail for you.")
                    utils.open_gmail()
                    logger.log(command, "open_gmail", "Gmail opened successfully.")
                
                elif "open browser" in command:
                    Nexa.speak("Opening your default web browser.")
                    utils.open_browser()
                    logger.log(command, "open_browser", "Web browser opened successfully.")
                
                elif "open linkedin" in command:
                    Nexa.speak("Opening LinkedIn for you.")
                    utils.open_linkedin()
                    logger.log(command, "open_linkedin", "LinkedIn opened successfully.")
                    
                elif "open facebook" in command:
                    Nexa.speak("Opening Facebook for you.")
                    utils.open_facebook()
                    logger.log(command, "open_facebook", "Facebook opened successfully.")
                
                elif "open github" in command:
                    Nexa.speak("Opening GitHub for you.")
                    utils.open_github()
                    logger.log(command, "open_github", "GitHub opened successfully.")
                
                elif "take screenshot" in command:
                    Nexa.speak("Taking a screenshot for you.")
                    screenshot_path = utils.take_screenshot()
                    Nexa.speak(f"Screenshot taken and saved as {screenshot_path}.")
                    logger.log(command, "take_screenshot", f"Screenshot saved at {screenshot_path}")
                
                elif "copy" in command:
                    text_to_copy = command.replace("copy", "").strip()
                    utils.copy_to_clipboard(text_to_copy)
                    Nexa.speak("Text copied to clipboard.")
                    logger.log(command, "copy", f"Copied text: {text_to_copy}")
                
                elif "paste" in command:
                    clipboard_content = utils.read_from_clipboard()
                    Nexa.speak(f"The clipboard contains: {clipboard_content}")
                    logger.log(command, "paste", f"Pasted text: {clipboard_content}")
                
                elif "lock screen" in command:
                    Nexa.speak("Locking your screen.")
                    utils.lock_screen()
                    logger.log(command, "lock_screen", "Screen locked successfully.")
                
                elif "type" in command:
                    text_to_type = command.replace("type", "").strip()
                    utils.type_text(text_to_type)
                    Nexa.speak("Typing the text for you.")
                    logger.log(command, "type_text", f"Typed text: {text_to_type}")
                
                elif "scroll up" in command:
                    utils.scroll_up()
                    Nexa.speak("Scrolled up.")
                    logger.log(command, "scroll_up", "Scrolled up successfully.")
                
                elif "scroll down" in command:
                    utils.scroll_down()
                    Nexa.speak("Scrolled down.")
                    logger.log(command, "scroll_down", "Scrolled down successfully.")
                
                elif "switch app" in command:
                    utils.switch_window()
                    Nexa.speak("Switched to the next app.")
                    logger.log(command, "switch_window", "Switched to the next app successfully.")

                elif "exit" in command or "quit" in command:
                    Nexa.speak("Goodbye!")
                    is_running = False
        