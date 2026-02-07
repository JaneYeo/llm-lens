#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
from db_client import upsert_post

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

FACTS_DIR = os.path.join(os.getcwd(), '.tmp', 'facts')
FEED_DIR = os.path.join(os.getcwd(), 'web', 'public', 'feed')

def ensure_dirs():
    if not os.path.exists(FEED_DIR):
        os.makedirs(FEED_DIR)

def sync_facts_to_db():
    print("Syncing facts to Database...")
    
    if not os.path.exists(FACTS_DIR):
        print("No facts directory found.")
        return

    fact_files = [f for f in os.listdir(FACTS_DIR) if f.endswith('.json')]
    print(f"Found {len(fact_files)} fact files")
    
    synced_count = 0
    for filename in fact_files:
        fact_path = os.path.join(FACTS_DIR, filename)
        try:
            with open(fact_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Construct Post Object
            post = {
                "id": data.get("id"),
                "headline": data.get("facts", {}).get("headline", data.get("title")),
                "summary": data.get("facts", {}).get("simple_explanation", ""),
                # Construct a rich context for the chatbot
                "full_content": (
                    f"Headline: {data.get('title')}\n"
                    f"Source: {data.get('source')}\n\n"
                    f"Analysis: {json.dumps(data.get('analysis', {}), indent=2)}\n\n"
                    f"Key Facts: {json.dumps(data.get('facts', {}), indent=2)}"
                ),
                "impact_score": 80, # Default high
                "visual_path": data.get("image_url"), # Ideally this is set by create_visual.py
                "source": data.get("source"),
                "metadata": data,
                "created_at": data.get("published") # Use published date if available
            }
            
            upsert_post(post)
            synced_count += 1
            
            # Legacy: Also keep JSON feed updated for static access if needed
            public_json_path = os.path.join(FEED_DIR, filename)
            with open(public_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error syncing {filename}: {e}")

    print(f"Successfully synced {synced_count} items to DB.")

def main():
    ensure_dirs()
    while True:
        sync_facts_to_db()
        print("Sleeping for 10s...")
        time.sleep(10)

if __name__ == "__main__":
    main()
