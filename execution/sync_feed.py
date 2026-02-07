#!/usr/bin/env python3
import os
import json
import time
import shutil

FACTS_DIR = os.path.join(os.getcwd(), '.tmp', 'facts')
FEED_DIR = os.path.join(os.getcwd(), 'web', 'public', 'feed')

def ensure_dirs():
    if not os.path.exists(FEED_DIR):
        os.makedirs(FEED_DIR)

def sync():
    ensure_dirs()
    if not os.path.exists(FACTS_DIR):
        return

    feed_items = []
    
    # List all facts
    fact_files = [f for f in os.listdir(FACTS_DIR) if f.endswith('.json')]
    
    for filename in fact_files:
        fact_path = os.path.join(FACTS_DIR, filename)
        with open(fact_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Check if image exists
        base_name = filename.replace('.json', '.png')
        image_path = os.path.join(FEED_DIR, base_name)
        
        # Add to feed even if image is missing (fallback to text-only)
        if os.path.exists(image_path):
            data['image_url'] = f"/feed/{base_name}"
        else:
            data['image_url'] = None
            
        feed_items.append(data)
        
        # Also save individual JSON to public feed for static access if needed
        public_json_path = os.path.join(FEED_DIR, filename)
        with open(public_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    # Sort by date (published) descending
    feed_items.sort(key=lambda x: x.get('published', ''), reverse=True)
    
    # Write index.json
    index_path = os.path.join(FEED_DIR, 'index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(feed_items, f, indent=2)
        
    print(f"Synced {len(feed_items)} items to feed.")

def main():
    print("Starting Feed Sync Service...")
    while True:
        try:
            sync()
        except Exception as e:
            print(f"Error syncing feed: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()
