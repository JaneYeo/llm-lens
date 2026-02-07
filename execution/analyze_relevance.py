#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Lens Relevance Analysis Agent
Uses Gemini 3 Pro to score articles and determine if they are infographic-worthy.
Operates on the database.
"""
import os
import sys
import json
import time
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Load env variables
load_dotenv()

sys.path.append(str(Path(__file__).parent))
from database import get_articles_by_status, update_article_status

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-3-pro-preview"

def analyze_article(article_data):
    """
    Uses Gemini to analyze relevance and extract category/reasoning.
    """
    prompt = f"""
    Analyze the following news item for use in an "AI Industry Infographic Feed".
    
    Title: {article_data.get('title')}
    Source: {article_data.get('source')}
    Summary: {article_data.get('summary')}
    
    Determine:
    1. Relevance Score (0-10): How significant is this to the AI/LLM/Hardware industry?
    2. Category: one of [Model Release, Chip Advancement, Industry Shift, Application, Research, Other]
    3. Infographic Worthy: true/false (Is there enough substance/impact for a visual?)
    4. Reasoning: Brief explanation.
    
    Return result in JSON format:
    {{
        "relevance_score": int,
        "category": "string",
        "infographic_worthy": boolean,
        "reasoning": "string"
    }}
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID, 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error analyzing {article_data.get('id')}: {e}")
        return None

def main():
    print(f"Starting Relevance Analysis using {MODEL_ID}...")
    
    # Fetch pending articles
    pending = get_articles_by_status('ingested', limit=50)
    print(f"Found {len(pending)} articles to analyze.")
    
    processed_count = 0
    relevant_count = 0
    
    for article in pending:
        print(f"Analyzing: {article.get('title', 'Unknown')[:50]}...")
        analysis = analyze_article(article)
        
        if analysis:
            score = analysis.get('relevance_score', 0)
            is_worthy = analysis.get('infographic_worthy', False)
            
            # Save if relevant: score >= 3 OR explicitly marked as infographic_worthy
            is_relevant = (score >= 3 or is_worthy)
            
            if is_relevant:
                update_article_status(article['id'], 'filtered', {'analysis': analysis})
                relevant_count += 1
                print(f"  -> RELEVANT (Score: {score}, Worthy: {is_worthy})")
            else:
                update_article_status(article['id'], 'ignored', {'analysis': analysis})
                print(f"  -> IGNORED (Score: {score})")
                
            processed_count += 1
            time.sleep(1) # Rate limit politeness
        else:
            print(f"  -> Failed to analyze.")
        
    print(f"Analysis complete. Analyzed {processed_count}, Found {relevant_count} relevant items.")

if __name__ == "__main__":
    main()
