import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class utils:
    def __init__(self):
        self.search_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.search_engine_id = os.getenv("SEARCH_ENGINE_ID")
        self.service = build("customsearch", "v1", developerKey=self.search_key)

    def google_search(self, query):
        try:
            res = self.service.cse().list(q=query, cx=self.search_engine_id).execute()
            print(res)
            return res['items'][0]['snippet']
        except Exception as e:
            print(f"An error occurred during Google Search: {e}")
            return "Sorry, I couldn't fetch the information right now."
        
search_utils = utils()
search_utils.google_search("What is the capital of France?")