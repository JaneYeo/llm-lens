#!/usr/bin/env python3
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

try:
    print("Listing models (filtered)...")
    for m in client.models.list(config={"page_size": 100}):
        if any(x in m.name.lower() for x in ['gemini', 'banana', 'pro']):
            print(f"Model: {m.name}")
except Exception as e:
    print(f"Error: {e}")
