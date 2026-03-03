from queue import Queue
import threading
from datetime import datetime
from tts import NexaSpeaker
from listener import NexaListener
from langchain.messages import HumanMessage, AIMessage
from logger import Logger
from random import choice
from agent import agent

logger = Logger()


def listener_thread(listener: NexaListener, command_queue: Queue):
    """Continuously listen for voice commands and push them into a shared queue."""
    while True:
        command = listener.listen()
        if command:
            command_queue.put(command)


starter_lines = [
    "Initializing Nexa. Ready to assist you.",
]

sleep_lines = [
    "Nexa is going to sleep. Say 'Nexa wake up' to wake me.",
    "Entering sleep mode. I'll be quiet until you call me.",
    "Nexa is taking a nap. I'll be here when you wake me up.",
]

wake_lines = [
    "Nexa is awake and ready to assist you.",
    "Back online! What can I do for you?",
    "Nexa is awake and listening. How can I help you?",
    "Nexa is back and ready to assist. What do you need?",
]


def extract_ai_response(agent_result) -> str:
    """
    Extract the latest AI response text from the LangGraph agent result.
    Expects a dict like {"messages": [...]} and returns the content of the last AIMessage.
    """
    try:
        messages = agent_result.get("messages", [])
        if not messages:
            return "I'm sorry, I couldn't generate a response."

        last_msg = messages[-1]

        # When running via LangChain / LangGraph, messages may be BaseMessage instances
        if isinstance(last_msg, AIMessage):
            return last_msg.content

        # Fallback if it's a dict-like structure
        content = getattr(last_msg, "content", None) or last_msg.get("content")
        return content or "I'm sorry, I couldn't generate a response."
    except Exception:
        return "I ran into an issue while generating a response."


def main():
    Nexa = NexaSpeaker()
    is_awake = True

    init_line = choice(starter_lines)
    print(f"[Nexa] {init_line}")
    Nexa.speak(init_line)

    listener = NexaListener()
    command_queue = Queue()

    # Background thread that continuously fills the queue with recognized commands
    t = threading.Thread(
        target=listener_thread,
        args=(listener, command_queue),
        daemon=True,
    )
    t.start()

    while True:
        # NOTE: For testing, we keep this hardcoded command.
        # To use live voice input instead, uncomment the two lines below and remove the hardcoded command.
        # command = command_queue.get()
        # print(f"[Nexa] Heard: {command}")
        # command = command.lower()
        command = "Nexa Who is current prime minister of Pakistan"

        if not command:
            continue

        print(f"[Nexa] Processing command: {command}")

        # Basic wake/sleep handling
        if "go to sleep" in command:
            if is_awake:
                is_awake = False
                line = choice(sleep_lines)
                print(f"[Nexa] Going to sleep: {line}")
                logger.log(command, "sleep", line)
                Nexa.speak(line)
            continue

        if ("wake up" in command) or ("nexa" in command and not is_awake):
            if not is_awake:
                is_awake = True
                line = choice(wake_lines)
                print(f"[Nexa] Waking up: {line}")
                logger.log(command, "wake", line)
                Nexa.speak(line)
            continue

        if not is_awake and ("wake up" not in command):
            # Ignore any commands while sleeping unless explicitly asked to wake up
            print("[Nexa] Ignoring command while asleep.")
            continue

        try:
            print("[Nexa] Sending command to agent...")
            result = agent.invoke({"messages": [HumanMessage(content=command)]})
            reply_text = extract_ai_response(result)
            print(f"[Nexa] Agent reply: {reply_text}")
            logger.log(command, "agent_invoke", reply_text)
            Nexa.speak(reply_text)
        except Exception as e:
            error_msg = f"Something went wrong while processing your request: {e}"
            print(f"[Nexa] ERROR: {error_msg}")
            logger.log(command, "error", str(e))
            Nexa.speak(error_msg)


if __name__ == "__main__":
    main()