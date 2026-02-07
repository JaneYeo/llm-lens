#!/usr/bin/env python3
"""
Upload generated visuals to Cloudinary and update database.
Run this after generate_ai_visuals.py in the cloud.
"""
import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

sys.path.append(str(Path(__file__).parent))
from database import get_connection, update_article_status

# Load env variables
load_dotenv()

# Cloudinary Config
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
if not CLOUDINARY_URL:
    print("Warning: CLOUDINARY_URL not set. Skipping upload.")
    sys.exit(0)

def main():
    print("Starting Visual Upload Sync...")
    
    # 1. Find all local images in PUBLIC_FEED
    feed_dir = Path('web/public/feed')
    if not feed_dir.exists():
        print("No feed directory found.")
        return

    # 2. Get DB connection
    conn = get_connection()
    cursor = conn.cursor()
    
    # 3. Find articles that are 'visualized' but have a local file path
    # We want to replace '/feed/xyz.png' with 'https://res.cloudinary...'
    cursor.execute("SELECT id, image_path FROM articles WHERE status = 'visualized' AND image_path LIKE '/feed/%'")
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} visuals needing cloud upload.")
    
    for row in rows:
        article_id = row['id']
        local_rel_path = row['image_path'].lstrip('/') # e.g. feed/xyz.png
        local_full_path = Path('web/public') / local_rel_path
        
        if not local_full_path.exists():
            print(f"File missing for {article_id}: {local_full_path}")
            continue
            
        print(f"Uploading {local_full_path.name}...")
        try:
            # Upload to Cloudinary
            response = cloudinary.uploader.upload(str(local_full_path), 
                folder="llm_lens_feed",
                public_id=local_full_path.stem,
                overwrite=True
            )
            
            secure_url = response['secure_url']
            print(f"  -> Uploaded: {secure_url}")
            
            # Update DB
            update_article_status(article_id, 'visualized', {'image_path': secure_url})
            
            # Optional: Delete local file to save space? 
            # local_full_path.unlink() 
            
        except Exception as e:
            print(f"  ✗ Upload failed: {e}")
            
    print("Upload sync complete.")

if __name__ == "__main__":
    main()
