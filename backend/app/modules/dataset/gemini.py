import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

class Gemini:
    def __init__(self):
        load_dotenv()
        # api_key = os.environ.get("GOOGLE_API_KEY")
        api_key = "AIzaSyBSVIWVGiIo8F7E_5Q0NgN70OGARnHbh5Q"
        self.token_size = 900_000
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not set.")
            exit()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")


    def prompt(self, message):
        return self.model.generate_content(message)


