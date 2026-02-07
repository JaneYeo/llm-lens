import os
import sys
import json
from pathlib import Path
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).parent / 'execution'))
import database
from distill_facts import distill_article

def test():
    database.init_db()
    pending = database.get_articles_by_status('ingested', limit=1)
    if not pending:
        print("No ingested articles found.")
        return
    
    art = pending[0]
    print(f"Testing ArXiv/Article: {art['title']}")
    
    try:
        facts = distill_article(art)
        print(f"Result facts: {json.dumps(facts, indent=2)}")
    except Exception as e:
        print(f"Distillation error: {e}")

if __name__ == "__main__":
    test()
