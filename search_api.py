import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
class NexaSearch:
    def __init__(self):
        self.client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
        )
    
    def search(self, query):
        response = self.client.models.generate_content(
            model="gemini-2.5",
            contents=f"You are an expert researcher and give information on facts only, answr this query: \"{query}\" and you last limit of maximum sentences is 12 you always try to give shortest and to the point answer to the query and barely use 9 to 12 sentences."
        )
        data = response.text
        summary = self.summarize(data) 
        return {"response": summary}
    
    def generate_image(self, query):
        response = self.client.models.generate_image(
            model="nano-banana-pro-preview",
            content=query
        )

        return {"image": response}
    
    def summarize(self, query):
        summary = self.client.models.generate_content(
            model="gemini-2.5",
            content=f"You are an Nexa AI powered desktop assistant, make a well defined and top notch summary of this query: {query} not more than 7 sentences and make summary without commentary"
        )

        return summary.text