import os
from dotenv import load_dotenv
from google import genai
from tts import NexaSpeaker

load_dotenv()
class NexaSearch:
    def __init__(self):
        self.client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
        )
    
    def search(self, query):
        try:        
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
contents=f"""Answer the user query using only verifiable facts.
and give predictions and facts only when user asks for it.,
Provide a tight response in 1 to 3 sentences (extendable if necessary for clarity).
Avoid unnecessary words, commentary, or filler.
Query: "{query}" """)

            data = getattr(response, "text", "")
            print(data)
            return {"response": data}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"response": "Sorry, I couldn't fetch the information right now."}
    
    def generate_image(self, query):
        response = self.client.models.generate_image(
            model="nano-banana-pro-preview",
            contents=query
        )

        return {"image": response}