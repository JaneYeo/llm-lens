import os
import json
from google import genai
from dotenv import load_dotenv
load_dotenv()

def debug_distill():
    api_key = os.getenv('GOOGLE_API_KEY')
    print(f"Using key starting with: {api_key[:10]}...")
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Extract JSON: { 'test': 'hello' }"
        )
        print("1.5-Flash Response:", response.text)
    except Exception as e:
        print("1.5-Flash Error:", e)

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents="Extract JSON: { 'test': 'hello' }"
        )
        print("Gemini-3 Response:", response.text)
    except Exception as e:
        print("Gemini-3 Error:", e)

if __name__ == "__main__":
    debug_distill()
