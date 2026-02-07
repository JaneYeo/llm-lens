#!/usr/bin/env python3
"""Remove duplicate posts from database, keeping only the most recent version."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from db_client import get_db

def deduplicate_posts():
    """Remove duplicate posts based on headline, keeping the most recent."""
    db = get_db()
    cursor = db.cursor()
    
    # Find duplicates
    cursor.execute('''
        SELECT headline, COUNT(*) as cnt 
        FROM posts 
        GROUP BY headline 
        HAVING cnt > 1 
        ORDER BY cnt DESC
    ''')
    
    duplicates = cursor.fetchall()
    print(f"Found {len(duplicates)} duplicate headlines")
    
    total_removed = 0
    for headline, count in duplicates:
        print(f"\nProcessing: {headline[:60]}... ({count} copies)")
        
        # Get all posts with this headline, ordered by created_at
        cursor.execute('''
            SELECT id, created_at FROM posts 
            WHERE headline = ? 
            ORDER BY created_at DESC
        ''', (headline,))
        
        posts = cursor.fetchall()
        
        # Keep the first (most recent), delete the rest
        keep_id = posts[0][0]
        to_delete = [p[0] for p in posts[1:]]
        
        print(f"  Keeping: {keep_id[:8]}... (created: {posts[0][1][:10]})")
        print(f"  Removing {len(to_delete)} duplicates...")
        
        for post_id in to_delete:
            cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
            total_removed += 1
    
    db.commit()
    db.close()
    
    print(f"\n✅ Deduplication complete!")
    print(f"   Removed: {total_removed} duplicate posts")
    print(f"   Unique titles: {len(duplicates)}")

if __name__ == "__main__":
    deduplicate_posts()
