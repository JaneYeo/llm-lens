import os
import sqlite3
from pathlib import Path

DB_PATH = Path("llm_lens.db")
FEED_DIR = Path("web/public/feed")

def cleanup():
    if not DB_PATH.exists():
        print("DB not found")
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get all articles with an image_path
    c.execute("SELECT id, title, image_path FROM articles WHERE image_path IS NOT NULL AND image_path != ''")
    articles = c.fetchall()
    
    cleared_count = 0
    for art in articles:
        path_str = art['image_path']
        # Path is like /feed/filename.png
        if path_str.startswith('/feed/'):
            filename = path_str[6:]
            file_path = FEED_DIR / filename
            if not file_path.exists():
                print(f"File missing: {filename}. Clearing DB path for {art['title'][:30]}...")
                c.execute("UPDATE articles SET image_path = NULL, status = 'distilled' WHERE id = ?", (art['id'],))
                cleared_count += 1
                
    conn.commit()
    conn.close()
    print(f"Finished. Cleared {cleared_count} invalid records from articles table.")

if __name__ == "__main__":
    cleanup()
