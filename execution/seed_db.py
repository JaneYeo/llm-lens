import json
from pathlib import Path
from db_client import upsert_post

FEED_PATH = Path("web/public/feed/index.json")

def seed():
    if not FEED_PATH.exists():
        print("No feed found.")
        return

    with open(FEED_PATH, 'r') as f:
        items = json.load(f)

    for item in items:
        # Map JSON structure to DB Schema
        post = {
            "id": item.get("id"),
            "headline": item.get("facts", {}).get("headline", item.get("title")),
            "summary": item.get("facts", {}).get("simple_explanation", ""),
            "full_content": f"Full context for {item.get('title')}. Source: {item.get('source')}. Stats: {item.get('facts', {}).get('key_stats', [])}", # Placeholder for now
            "impact_score": 85, # Default high score for existing items
            "visual_path": item.get("image_url"),
            "source": item.get("source"),
            "metadata": item
        }
        upsert_post(post)
        print(f"Inserted: {post['headline']}")

if __name__ == "__main__":
    seed()
