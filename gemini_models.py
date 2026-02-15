import requests
import os

API_KEY = os.environ.get("GOOGLE_API_KEY")

response = requests.get(
    "https://generativelanguage.googleapis.com/v1beta/models",
    headers={"x-goog-api-key": "AIzaSyDOQmyIVLvLAwVg6NIFYRmLJnGIuYy7FRg"}
)

models = response.json()
for model in models.get("models", []):
    print(model["name"])
