#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import shutil

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

RAW_DIR = os.path.join(os.getcwd(), '.tmp', 'raw_news')
FILTERED_DIR = os.path.join(os.getcwd(), '.tmp', 'filtered_news')

def ensure_dirs():
    if not os.path.exists(FILTERED_DIR):
        os.makedirs(FILTERED_DIR)

def main():
    ensure_dirs()
    print("Bypassing relevance filter - copying all articles...")
    
    raw_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.json')]
    copied_count = 0
    
    for filename in raw_files:
        raw_path = os.path.join(RAW_DIR, filename)
        filtered_path = os.path.join(FILTERED_DIR, filename)
        
        # Skip if already exists
        if os.path.exists(filtered_path):
            continue
        
        # Load article
        with open(raw_path, 'r', encoding='utf-8') as f:
            article = json.load(f)
        
        # Add dummy analysis
        article['analysis'] = {
            'relevance_score': 8,  # Assume all are relevant
            'category': 'AI News',
            'infographic_worthy': True,
            'reasoning': 'Bypassed filter for testing'
        }
        
        # Save to filtered
        with open(filtered_path, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2)
        
        copied_count += 1
    
    print(f"Bypass complete. Copied {copied_count} articles to {FILTERED_DIR}")
    print(f"Total articles in filtered_news: {len([f for f in os.listdir(FILTERED_DIR) if f.endswith('.json')])}")

if __name__ == "__main__":
    main()
