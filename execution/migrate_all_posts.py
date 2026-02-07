#!/usr/bin/env python3
"""Migrate all filtered news from .tmp/filtered_news to database."""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))
from db_client import upsert_post, init_db

def migrate_filtered_news():
    """Import all filtered news articles into the database."""
    init_db()
    
    filtered_dir = Path('.tmp/filtered_news')
    if not filtered_dir.exists():
        print("No filtered_news directory found")
        return
    
    json_files = list(filtered_dir.glob('*.json'))
    print(f"Found {len(json_files)} filtered news files")
    
    migrated = 0
    skipped = 0
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract key information
            post_id = data.get('id')
            if not post_id:
                skipped += 1
                continue
            
            title = data.get('title', 'Unknown')
            summary = data.get('summary', '')
            source = data.get('source', 'Unknown')
            published = data.get('published', datetime.now().isoformat())
            
            # Build rich context for chatbot
            analysis = data.get('analysis', {})
            full_content = f"""
Title: {title}
Source: {source}
Published: {published}

Summary: {summary}

Analysis:
- Relevance Score: {analysis.get('relevance_score', 'N/A')}/10
- Category: {analysis.get('category', 'General')}
- Infographic Worthy: {analysis.get('infographic_worthy', False)}
- Reasoning: {analysis.get('reasoning', 'Not provided')}

Full Article:
{summary}
            """.strip()
            
            post = {
                "id": post_id,
                "headline": title,
                "summary": summary,
                "full_content": full_content,
                "impact_score": int(analysis.get('relevance_score', 5) * 10),  # Scale to 0-100
                "visual_path": None,  # Will be generated later
                "source": source,
                "created_at": published,
                "metadata": data
            }
            
            upsert_post(post)
            migrated += 1
            
            if migrated % 10 == 0:
                print(f"Migrated {migrated} posts...")
                
        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
            skipped += 1
    
    print(f"\n✅ Migration complete!")
    print(f"   Migrated: {migrated}")
    print(f"   Skipped: {skipped}")
    print(f"   Total: {migrated + skipped}")

if __name__ == "__main__":
    migrate_filtered_news()
