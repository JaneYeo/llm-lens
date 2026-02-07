import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = Path("llm_lens.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            headline TEXT,
            summary TEXT,
            full_content TEXT,
            impact_score INTEGER,
            visual_path TEXT,
            source TEXT,
            created_at TIMESTAMP,
            metadata TEXT
        )
    ''')
    conn.commit()
    conn.close()

def upsert_post(data):
    """
    Insert or update a post. 
    data: dict containing post fields.
    """
    conn = get_db()
    c = conn.cursor()
    
    # Generate ID if not present (hash of headline usually better for dedup, but UUID for now)
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
        
    now = datetime.now().isoformat()
    
    c.execute('''
        INSERT INTO posts (id, headline, summary, full_content, impact_score, visual_path, source, created_at, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            headline=excluded.headline,
            summary=excluded.summary,
            full_content=excluded.full_content,
            visual_path=excluded.visual_path,
            impact_score=excluded.impact_score
    ''', (
        data['id'],
        data.get('headline'),
        data.get('summary'),
        data.get('full_content', ''),
        data.get('impact_score', 0),
        data.get('visual_path'),
        data.get('source', 'Unknown'),
        data.get('created_at', now),
        json.dumps(data.get('metadata', {}))
    ))
    
    conn.commit()
    conn.close()
    return data['id']

def get_recent_posts(limit=20):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM posts ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_post_by_id(post_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def get_pending_visuals(limit=5):
    conn = get_db()
    c = conn.cursor()
    # Find posts where visual_path is NULL or empty
    c.execute("SELECT * FROM posts WHERE visual_path IS NULL OR visual_path = '' ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
