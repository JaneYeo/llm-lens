#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import database  # Import DB module

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

FEED_DIR = os.path.join(os.getcwd(), 'web', 'public', 'feed')
# FACTS_DIR deprecated

def critique_image(image_path, fact_data):
    """
    Uses Gemini Vision to critique the generated image.
    """
    print(f"Critiquing: {os.path.basename(image_path)}...")
    
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = f"""
    You are an expert design and fact-checking agent for "LLM Lens".
    Critique this generated infographic based on the source facts.
    
    SOURCE FACTS:
    - Headline: {fact_data.get('facts', {}).get('headline')}
    - Key Stats: {fact_data.get('facts', {}).get('key_stats')}
    
    CRITIQUE TASKS:
    1. Perform OCR on the image. Does the text match the facts accurately?
    2. Evaluate readability. Is the text clear or garbled?
    3. Evaluate visual style (must be Futurist, High-Tech, Neon Dark Mode).
    
    Output JSON format:
    {{
        "score": int (0-10),
        "readability": "string (Good/Fair/Poor)",
        "accuracy_warning": "string or null",
        "critique_summary": "string",
        "regeneration_required": boolean
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=[prompt, types.Part.from_bytes(data=image_bytes, mime_type="image/png")],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error critiquing {image_path}: {e}")
        return None

def main():
    database.init_db()
    
    # Logic: Get articles that are visualized but NOT yet critiqued
    # Since our simple get_articles_by_status doesn't filter by "not critiqued",
    # we'll fetch 'visualized' and check the critique_json field in Python.
    articles = database.get_articles_by_status('visualized', limit=50)
    
    print(f"Checking {len(articles)} articles for critique needs...")
    updated_count = 0

    for article in articles:
        # Skip if already critiqued (check dict key)
        if article.get('critique_json'):
            continue
            
        print(f"Processing: {article.get('title', 'Unknown')[:50]}...")
        
        # We need the facts to critique against
        if isinstance(article.get('facts_json'), str):
            facts_data = json.loads(article['facts_json'])
        else:
            facts_data = article.get('facts_json')
            
        # We need the image path (local relative path stored in DB is /feed/xyz.png)
        # We need to resolve this to absolute system path for opening
        db_image_path = article.get('image_path')
        if not db_image_path:
            continue
            
        filename = os.path.basename(db_image_path)
        local_image_path = os.path.join(FEED_DIR, filename)
        
        if not os.path.exists(local_image_path):
            print(f"  Warning: Image not found at {local_image_path}")
            continue

        result = critique_image(local_image_path, {'facts': facts_data})
        if result:
            # Update DB with critique
            database.update_article_status(
                article['id'],
                'visualized', # Status remains visualized, or we could add 'critiqued'
                additional_data={'critique': result}
            )
            updated_count += 1
            print(f"  -> Score: {result.get('score')} (Regen: {result.get('regeneration_required')})")

    print(f"Self-critique complete. Updated {updated_count} records.")

if __name__ == "__main__":
    main()
