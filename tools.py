import webbrowser
import os
from xml.parsers.expat import model
import pyperclip
import pyautogui
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_tavily import TavilySearch
load_dotenv()


def google_search(query):
    """
    Docstring for tool:
    Use this tool when the user's query involves current events, recent news, or any information not known to the LLM.
    Provide the user's full question as input. Returns the most relevant answer from a real-time web search.
    """
    tavily_search_tool = TavilySearch(max_results=1,topic="general", language="en")
    search_results = tavily_search_tool.run(query)
    title = search_results["results"][0]['title']
    content = search_results["results"][0]["content"]
    url = search_results["results"][0]['url']
    print(content)
    return {"title": title, "content": content, "url": url}


@tool
def open_code():
    """Open Visual Studio Code on the local machine."""
    os.startfile("C:/Users/Hamza/AppData/Local/Programs/Microsoft VS Code/code.exe")
    return True


@tool
def open_gmail():
    """Open Gmail in the default web browser."""
    webbrowser.open("https://mail.google.com")
    return True


@tool
def open_browser():
    """Open Google Chrome browser."""
    os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
    return True


@tool
def open_linkedin():
    """Open LinkedIn website in the browser."""
    webbrowser.open("https://www.linkedin.com")
    return True


@tool
def open_github():
    """Open GitHub website in the browser."""
    webbrowser.open("https://www.github.com")
    return True


@tool
def open_facebook():
    """Open Facebook website in the browser."""
    webbrowser.open("https://www.facebook.com")
    return True


@tool
def copy_to_clipboard(text):
    """Copy the given text to the system clipboard."""
    pyperclip.copy(text)
    return True


@tool
def read_from_clipboard():
    """Read and return text from the system clipboard."""
    return pyperclip.paste()


@tool
def lock_screen():
    """Lock the Windows screen."""
    pyautogui.hotkey('win', 'l')
    return True


@tool
def type_text(text):
    """Type the given text at the current cursor position."""
    pyautogui.typewrite(text)
    return True


@tool
def scroll_up():
    """Scroll the screen up."""
    pyautogui.scroll(500)
    return True


# @tool
def scroll_down():
    """Scroll the screen down."""
    pyautogui.scroll(-500)
    return True


@tool
def take_screenshot():
    """Take a screenshot and save it to ./screenshots/screenshot.png."""
    screenshot = pyautogui.screenshot()
    screenshot.save("./screenshots/screenshot.png")
    return "screenshot.png"


@tool
def switch_window():
    """Switch to the next open window using Alt+Tab."""
    pyautogui.hotkey('alt', 'tab')
    return True


@tool
def open_chatgpt():
    """Open ChatGPT website in the browser."""
    webbrowser.open("https://chat.openai.com")
    return True