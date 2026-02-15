import webbrowser
import os
import pyperclip
import pyautogui
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Utils:

    def google_search(self, query):
        try:
            search_key = os.getenv("GOOGLE_SEARCH_API_KEY")
            search_engine_id = os.getenv("SEARCH_ENGINE_ID")
            service = build("customsearch", "v1", developerKey=search_key)
            res = service.cse().list(q=query, cx=search_engine_id).execute()
            print(res)
            return res['items'][0]['snippet']
        except Exception as e:
            print(f"An error occurred during Google Search: {e}")
            return "Sorry, I couldn't fetch the information right now."
    
    def open_code(self):
        os.startfile("C:/Users/Hamza/AppData/Local/Programs/Microsoft VS Code/code.exe")
        return True
    
    def open_gmail(self):
        webbrowser.open("https://mail.google.com")
        return True 
    
    def open_browser(self):
        os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
        return True
    
    def open_linkedin(self):
        webbrowser.open("https://www.linkedin.com")
        return True
    
    def open_github(self):
        webbrowser.open("https://www.github.com")
        return True
    
    def open_facebook(self):
        webbrowser.open("https://www.facebook.com")
        return True
    
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        return True
    
    def read_from_clipboard(self):
        return pyperclip.paste()

    def lock_screen(self):
        pyautogui.hotkey('win', 'l')
        return True
    
    def type_text(self, text):
        pyautogui.typewrite(text)
        return True
    
    def scroll_up(self):
        pyautogui.scroll(500)
        return True
    
    def scroll_down(self):
        pyautogui.scroll(-500)
        return True
    
    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("./screenshots/screenshot.png")
        return "screenshot.png"
    
    def switch_window(self):
        pyautogui.hotkey('alt', 'tab')
        return True
    
    def open_chatgpt(self):
        webbrowser.open("https://chat.openai.com")
        return True