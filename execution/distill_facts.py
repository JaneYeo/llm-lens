#!/usr/bin/env python3
"""
Distill core facts from news articles using Gemini 3 Flash.
Processes 'ingested' articles and moves them to 'distilled'.
"""
import os
import sys
import json
import time
from pathlib import Path
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).parent))
from database import get_articles_by_status, update_article_status

from dotenv import load_dotenv
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY'))

# UPGRADED TO GEMINI 3 FLASH for hackathon requirements
MODEL_ID = "gemini-3-flash-preview"

def distill_article(article_data, max_retries=3):
    """Call Gemini 3 to extract structured facts and a clean headline."""
    prompt = f"""
    Extract structured facts from this AI news item for an infographic.
    Use high-reasoning Gemini 3 insight to summarize effectively.
    
    IMPORTANT: If the source is 'ArXiv' or contains technical identifiers, CLEAN and SUMMARIZE.
    Remove strings like 'arXiv:2504.13376v4 Announce Type: replace-cross Abstract:'.
    Focus on: What they built, How it works, and Why it matters.
    
    Title: {article_data.get('title')}
    Summary: {article_data.get('summary')}
    Category: {article_data.get('source', 'Unknown')}
    
    Extract:
    1. Short Headline: Punchy, max 10 words. Strip all technical metadata/arXiv IDs.
    2. Key Stats: List 3+ strings (e.g. "98.5% Accuracy", "Reduced latency").
    3. Entities: Authors, Institutions, Companies.
    4. Simple Explanation: 2 sentences for a non-expert. Summarize long abstracts.
    5. Visual Concepts: 2 ideas for an icon/symbol (e.g. "Neural network graph").
    
    Return JSON:
    {{
        "headline": "string",
        "key_stats": ["string"],
        "entities": ["string"],
        "simple_explanation": "string",
        "visual_concepts": ["string"]
    }}
    """
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if not response.text:
                raise ValueError("Empty response text")
                
            facts = json.loads(response.text)
            return facts
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                wait_time = (attempt + 1) * 10
                print(f"  ! Quota hit (429). Retrying in {wait_time}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"Error distilling article with Gemini 3: {e}")
                break
    return None

def main():
    """Process pending articles in moderate batches."""
    pending = get_articles_by_status('filtered', limit=30)
    print(f"Found {len(pending)} articles to distill with {MODEL_ID}")
    
    distilled_count = 0
    for article in pending:
        # SKIP ArXiv articles as requested
        source = str(article.get('source', '')).lower()
        if 'arxiv' in source:
            print(f"Skipping ArXiv article: {article['title'][:40]}...")
            # Mark it as ignored or just leave it filtered? 
            # User said stop generating infographic, so we should skip it.
            update_article_status(article['id'], 'ignored', {})
            continue

        print(f"Distilling: {article['title'][:50]}...")
        facts = distill_article(article)
        
        if facts:
            # Update article with facts and change status
            update_article_status(article['id'], 'distilled', {'facts': facts})
            distilled_count += 1
            print(f"✓ Distilled (Gemini 3): {facts.get('headline')}")
        else:
            print(f"✗ Failed to distill: {article['id']}")
            
    print(f"\nDistilling finished. Finalized {distilled_count} articles using Gemini 3.")

if __name__ == "__main__":
    main()
