#!/usr/bin/env python3
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
print(f"Testing API with key: {API_KEY[:5]}...")

try:
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents="Hello, echo this back: 'API Working'"
    )
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
