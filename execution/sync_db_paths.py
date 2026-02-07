import os
import sqlite3
from pathlib import Path

DB_PATH = Path("llm_lens.db")
FEED_DIR = Path("web/public/feed")

def sync():
    if not DB_PATH.exists():
        print("DB not found")
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get all posts
    c.execute("SELECT id, headline, visual_path FROM posts")
    posts = c.fetchall()
    
    # Get all files on disk
    files = [f.name for f in FEED_DIR.glob("*.png")]
    print(f"Found {len(files)} files on disk.")
    
    updated_count = 0
    for post in posts:
        headline = post['headline'] or 'post'
        safe_title = "".join([c if c.isalnum() else "_" for c in headline])[:30] # Match create_visual.py logic
        
        # Try to find a file that starts with this safe_title
        match = None
        for f in files:
            if f.startswith(safe_title):
                match = f
                break
        
        if match:
            new_path = f"/feed/{match}"
            if post['visual_path'] != new_path:
                print(f"Updating {headline[:30]}: {post['visual_path']} -> {new_path}")
                c.execute("UPDATE posts SET visual_path = ? WHERE id = ?", (new_path, post['id']))
                updated_count += 1
        else:
            print(f"No match for: {headline[:30]}")
            
    conn.commit()
    conn.close()
    print(f"Finished. Updated {updated_count} records.")

if __name__ == "__main__":
    sync()
