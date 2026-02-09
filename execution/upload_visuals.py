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

# Ensure we can import from the current directory
sys.path.append(os.getcwd())
from execution.database import get_connection, update_article_status, row_to_dict

# Load env variables
load_dotenv()

# Cloudinary Config
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
if not CLOUDINARY_URL:
    print("Warning: CLOUDINARY_URL not set. Skipping upload.")
    sys.exit(0)

# Explicit configuration parsing
if CLOUDINARY_URL.startswith("cloudinary://"):
    # cloudinary://api_key:api_secret@cloud_name
    parts = CLOUDINARY_URL.replace("cloudinary://", "").split("@")
    if len(parts) == 2:
        creds, cloud_name = parts
        api_key, api_secret = creds.split(":")
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        print(f"Cloudinary configured for: {cloud_name}")
    else:
        print("Invalid CLOUDINARY_URL format.")
        sys.exit(1)
else:
    print("CLOUDINARY_URL must start with 'cloudinary://'")
    sys.exit(1)

def main():
    print("Starting Visual Upload Sync to Cloudinary...")
    
    # 1. Find all local images in PUBLIC_FEED
    feed_dir = Path('web/public/feed')
    if not feed_dir.exists():
        print("No feed directory found.")
        return

    # 2. Get DB connection
    conn = get_connection()
    cursor = conn.cursor()
    
    # 3. Find articles that are 'visualized' but have a local file path
    print("Querying database for local visuals...")
    cursor.execute("SELECT id, image_path FROM articles WHERE status = 'visualized' AND image_path LIKE '/feed/%'")
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} visuals needing cloud upload.")
    
    count = 0
    for row_raw in rows:
        row = row_to_dict(cursor, row_raw)
        article_id = row['id']
        image_path = row['image_path']
        
        if not image_path:
            continue
            
        local_rel_path = image_path.lstrip('/') # e.g. feed/xyz.png
        local_full_path = Path('web/public') / local_rel_path
        
        if not local_full_path.exists():
            # Try without public prefix in case it's different
            local_full_path = Path(local_rel_path)
            if not local_full_path.exists():
                print(f"  ✗ File missing for {article_id}: {local_rel_path}")
                continue
            
        print(f"Uploading {local_full_path.name} ({count+1}/{len(rows)})...")
        try:
            # Upload to Cloudinary
            # We use the filename as public_id for consistency
            response = cloudinary.uploader.upload(str(local_full_path), 
                folder="llm_lens_feed",
                public_id=local_full_path.stem,
                overwrite=True
            )
            
            secure_url = response['secure_url']
            print(f"    -> Success: {secure_url}")
            
            # Update DB with Cloud URL
            update_article_status(article_id, 'visualized', {'image_path': secure_url})
            count += 1
            
            # Rate limiting / polite pause
            if count % 10 == 0:
                time.sleep(1)
                
        except Exception as e:
            print(f"    ✗ Upload failed: {e}")
            
    print(f"Upload sync complete. {count} images pushed to Cloudinary.")

if __name__ == "__main__":
    main()
