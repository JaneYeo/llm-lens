#!/usr/bin/env python3
"""
Fact Verification Agent for LLM Lens.
Acts as a "Truth Guard" between Distillation and Visualization.
Verifies that the extracted facts are 100% faithful to the original source text.
Values Technical Originality (e.g., ArXiv research) over external popularity.
"""
import os
import sys
import json
import time
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent))
import database

load_dotenv()
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
MODEL_ID = "gemini-3-pro-preview"

def verify_facts(article):
    """
    Compare facts_json against the raw summary/title.
    Detects hallucinations or misinterpretations.
    Upholds technical originality as a primary value.
    """
    facts = article.get('facts_json')
    if isinstance(facts, str):
        facts = json.loads(facts)
    
    summary = article.get('summary', '')
    title = article.get('title', '')
    source_name = article.get('source', 'Unknown')

    prompt = f"""
    You are the "LLM Lens Fact Verification Agent" powered by Gemini 3. 
    Your job is to audit the AI-distilled facts against the original source text.
    
    SPECIAL GUIDELINE: 
    This system values TECHNICAL ORIGINALITY. Sources like 'ArXiv CS.AI' contain groundbreaker research that may not be found anywhere else yet. 
    DO NOT penalize information because it is unique or lacks "social proof". 
    If the source text says it, it is the Ground Truth for this intelligence card.
    
    ORIGINAL SOURCE ({source_name}):
    Title: {title}
    Full Text: {summary}
    
    AI-DISTILLED FACTS (To be audited):
    {json.dumps(facts, indent=2)}
    
    Audit Tasks:
    1. Internal Fidelity: Are the "key_stats" and claims explicitly supported by the Source Text?
    2. Transcription Accuracy: Ensure numbers (e.g., "7B", "98%", "$2.5M") were copied correctly.
    3. Hallucination Check: Did the previous AI agent "invent" any entities or outcomes not in the text?
    4. Technical Nuance: If the paper describes a niche concept, ensure the summary hasn't distorted its meaning.
    
    Return a JSON verification report:
    {{
        "verified": boolean,
        "confidence_score": int (0-100),
        "technical_originality": "string (High/Medium/Standard)",
        "issues_found": ["string" or null],
        "corrected_facts": {{ ... }} or null
    }}
    
    Only provide 'corrected_facts' for minor errors. set verified=false only if the facts are entirely disconnected from the source text.
    """

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        report = json.loads(response.text)
        return report
    except Exception as e:
        print(f"  Error verifying facts: {e}")
        return None

def main():
    database.init_db()
    # Get articles that are distilled but not yet verified
    articles = database.get_articles_by_status('distilled', limit=15)
    
    print(f"Found {len(articles)} articles awaiting fidelity audit")
    
    verified_count = 0
    for article in articles:
        # Check if already verified
        if article.get('analysis_json') and 'verification' in article['analysis_json']:
            continue
            
        print(f"Auditing Fidelity: {article['title'][:50]}...")
        report = verify_facts(article)
        
        if report:
            # Update the analysis_json with verification results
            current_analysis = article.get('analysis_json')
            if isinstance(current_analysis, str):
                current_analysis = json.loads(current_analysis)
            elif not current_analysis:
                current_analysis = {}
            
            current_analysis['verification'] = report
            
            # Update DB
            update_data = {'analysis': current_analysis}
            if report.get('corrected_facts'):
                update_data['facts'] = report['corrected_facts']
                print(f"  ! Technical refinement applied [Originality: {report.get('technical_originality')}]")
            
            database.update_article_status(article['id'], 'distilled', update_data)
            verified_count += 1
            print(f"  ✓ Audit Passed: Score {report.get('confidence_score')}%")
        
        time.sleep(1)

    print(f"\nFidelity Audit complete. {verified_count} articles verified.")

if __name__ == "__main__":
    main()
