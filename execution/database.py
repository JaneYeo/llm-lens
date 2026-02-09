#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Lens Database Module
Provides SQLite/Turso connectivity for accelerated news processing.
"""
import os
import sys
import json
import sqlite3
from datetime import datetime
import libsql
from dotenv import load_dotenv

load_dotenv()

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

DB_PATH = os.path.join(os.getcwd(), 'llm_lens.db')
TURSO_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

def get_connection():
    """Get a database connection (Local SQLite or Turso Cloud)."""
    if TURSO_URL and TURSO_TOKEN:
        try:
            # Connect to local file with sync to remote
            conn = libsql.connect("turso_cache.db", sync_url=TURSO_URL, auth_token=TURSO_TOKEN)
            conn.sync()
            # Turso connection doesn't support row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"Turso sync connection failed, falling back to local: {e}")
            
    # Pure local SQLite fallback
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(cursor, row):
    """Helper to convert a row to a dictionary if it isn't one already."""
    if isinstance(row, dict):
        return row
    if hasattr(row, 'keys'): # sqlite3.Row
        return dict(row)
    # Fallback for plain tuples (like from libsql)
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_db():
    """Initialize the database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Articles table (SQLite standard)
    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT UNIQUE,
            source TEXT,
            summary TEXT,
            published TEXT,
            fetched_at TEXT,
            status TEXT DEFAULT 'ingested',
            headline TEXT,
            analysis_json TEXT,
            facts_json TEXT,
            image_path TEXT,
            critique_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''
    
    cursor.execute(create_table_sql)
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON articles(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON articles(source)')
    
    conn.commit()
    if hasattr(conn, 'sync'): conn.sync()
    conn.close()
    mode = "Turso Cloud" if (TURSO_URL and TURSO_TOKEN) else "Local SQLite"
    print(f"Database initialized. Mode: {mode}")

def insert_article(article_data):
    """Insert a new article. Returns True if inserted, False if duplicate."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = '''
            INSERT INTO articles (id, title, url, source, summary, published, fetched_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'ingested')
        '''
        cursor.execute(query, (
            article_data.get('id'),
            article_data.get('title'),
            article_data.get('link') or article_data.get('url'),
            article_data.get('source'),
            article_data.get('summary'),
            article_data.get('published'),
            article_data.get('fetched_at', datetime.now().isoformat())
        ))
        conn.commit()
        if hasattr(conn, 'sync'): conn.sync()
        return True
    except Exception as e:
        if "UNIQUE" in str(e) or "PRIMARY KEY" in str(e):
            return False
        print(f"Error inserting article: {e}")
        return False
    finally:
        conn.close()

def get_articles_by_status(status, limit=100):
    """Get articles by their processing status."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM articles WHERE status = ? ORDER BY created_at DESC LIMIT ?', (status, limit))
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, row) for row in rows]
    conn.close()
    return result

def update_article_status(article_id, new_status, additional_data=None):
    """Update an article's status and optionally add data."""
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = ['status = ?', 'updated_at = ?']
    params = [new_status, datetime.now().isoformat()]
    
    if additional_data:
        if 'analysis' in additional_data:
            updates.append('analysis_json = ?')
            params.append(json.dumps(additional_data['analysis']))
        if 'facts' in additional_data:
            updates.append('facts_json = ?')
            params.append(json.dumps(additional_data['facts']))
        if 'image_path' in additional_data:
            updates.append('image_path = ?')
            params.append(additional_data['image_path'])
        if 'critique' in additional_data:
            updates.append('critique_json = ?')
            params.append(json.dumps(additional_data['critique']))
    
    params.append(article_id)
    
    cursor.execute(f'UPDATE articles SET {", ".join(updates)} WHERE id = ?', params)
    conn.commit()
    if hasattr(conn, 'sync'): conn.sync()
    conn.close()

def get_feed_articles(limit=50):
    """Get articles ready for the feed."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM articles 
        WHERE status = 'visualized' OR status = 'distilled'
        ORDER BY published DESC 
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, row) for row in rows]
    conn.close()
    return result

def get_stats():
    """Get processing statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT status, COUNT(*) as count FROM articles GROUP BY status')
    rows = cursor.fetchall()
    result = {row_to_dict(cursor, row)['status']: row_to_dict(cursor, row)['count'] for row in rows}
    conn.close()
    return result

if __name__ == "__main__":
    init_db()
