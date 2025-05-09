from typing import Union
from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# START SERVER WITH: fastapi dev simple_api.py --port 8080

app = FastAPI()
origins = [
    "http://localhost:5173",  # or http://localhost:8080 depending on your Vue dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # use ["*"] to allow all during testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{prompt}")
def read_root(prompt):
    response = model.generate_content(prompt)
    return {"response": response.text}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}