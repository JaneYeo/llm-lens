import os
import json
from google import genai
from dotenv import load_dotenv
load_dotenv()

def debug_models():
    api_key = os.getenv('GOOGLE_API_KEY')
    client = genai.Client(api_key=api_key)
    
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-2.0-flash-exp",
        "gemini-3-flash-preview",
        "gemini-3-pro-preview",
        "gemini-flash-latest"
    ]
    
    for m in models_to_test:
        try:
            print(f"Testing model: {m}...")
            response = client.models.generate_content(
                model=m,
                contents="test"
            )
            print(f"  ✓ {m} working!")
        except Exception as e:
            print(f"  ✗ {m} failed: {e}")

if __name__ == "__main__":
    debug_models()
