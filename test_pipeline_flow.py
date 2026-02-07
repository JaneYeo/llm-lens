import os
import sys
import json
import time
from pathlib import Path
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).parent / 'execution'))
import database
from distill_facts import distill_article

# OVERRIDE MODEL for speed test
import distill_facts
distill_facts.model_id = "gemini-1.5-flash"

def test_full_pipeline():
    database.init_db()
    # 1. Get one ingested
    pending = database.get_articles_by_status('ingested', limit=1)
    if not pending:
        print("No ingested articles found.")
        return
    
    art = pending[0]
    print(f"Step 1: Distilling {art['title'][:40]}...")
    facts = distill_article(art)
    
    if facts:
        # 2. Update to distilled
        database.update_article_status(art['id'], 'distilled', {'facts': facts})
        print(f"Step 2: Distilled successfully. Headline: {facts.get('headline')}")
        
        # 3. Generate Visual (calling the script logic)
        from generate_ai_visuals import generate_infographic
        output_dir = Path('web/public/feed')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        safe_title = "".join([c if c.isalnum() else "_" for c in art['title']])[:30]
        filename = f"TEST_{safe_title}_{art['id'][:8]}.png"
        output_path = output_dir / filename
        
        # Get revised article data from DB
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (art['id'],))
        updated_art = dict(cursor.fetchone())
        conn.close()
        
        print(f"Step 3: Generating Visual with Nano Banana Pro...")
        if generate_infographic(updated_art, str(output_path)):
            database.update_article_status(art['id'], 'visualized', {'image_path': f"/feed/{filename}"})
            print(f"Step 4: Full flow complete. Post {art['id']} is visualized.")
            print(f"Verify at: http://localhost:3000/dashboard")
        else:
            print("Step 3: Failed visual generation.")
    else:
        print("Step 1: Failed distillation.")

if __name__ == "__main__":
    test_full_pipeline()
