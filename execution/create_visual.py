#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from db_client import get_pending_visuals, upsert_post

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

FEED_DIR = os.path.join(os.getcwd(), 'web', 'public', 'feed')
MAX_IMAGES = 10 

def ensure_dirs():
    if not os.path.exists(FEED_DIR):
        os.makedirs(FEED_DIR)

def generate_visual_prompt(post):
    # Parse metadata if it's a string
    metadata = post.get('metadata')
    if isinstance(metadata, str):
        metadata = json.loads(metadata)
    
    analysis = metadata.get('analysis', {})
    facts = metadata.get('facts', {})

    text_prompt = f"""
    Create a detailed image generation prompt for an infographic based on these facts:
    Headline: {post.get('headline')}
    Summary: {post.get('summary')}
    Stats: {facts.get('key_stats', [])}
    Category: {analysis.get('category', 'Technology')}
    
    The style should be: "Nano Banana Pro Style", Futurist High-Tech, Dark Mode, Neon Accents, Glassmorphism, Data Visualization, 3D Render.
    Focus on VISUALIZING the numbers and the impact.
    
    Output ONLY the prompt text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=text_prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating prompt: {e}")
        return None

def generate_image(prompt, filename):
    print(f"Generating image with prompt: {prompt[:50]}...")
    try:
        response = client.models.generate_image(
            model="gemini-2.0-flash-exp-image-generation",
            prompt=prompt,
            config=types.GenerateImageConfig(
                number_of_images=1,
                aspect_ratio="3:4" 
            )
        )
        
        if response.generated_images:
            image = response.generated_images[0]
            image.save(filename)
            print(f"Saved to {filename}")
            return True
            
    except Exception as e:
        print(f"Error generating image: {e}")
        return False

def main():
    ensure_dirs()
    
    pending = get_pending_visuals(limit=MAX_IMAGES)
    print(f"Found {len(pending)} posts needing visuals...")
    
    generated_count = 0
    
    for post in pending:
        print(f"\nProcessing Visuals for: {post.get('headline', 'Unknown')[:60]}...")
        
        # Prepare filename
        safe_title = "".join([c if c.isalnum() else "_" for c in post['headline'] or 'post'])[:50]
        base_name = f"{safe_title}_{post['id'][:8]}.png"
        image_path = os.path.join(FEED_DIR, base_name)
        
        # Check if file already exists locally (skip gen if so)
        if os.path.exists(image_path):
            print("Image already exists locally... updating DB path.")
            post['visual_path'] = f"/feed/{base_name}"
            upsert_post(post)
            continue

        visual_prompt = generate_visual_prompt(post)
        if visual_prompt:
            success = generate_image(visual_prompt, image_path)
            if success:
                # Update DB
                post['visual_path'] = f"/feed/{base_name}"
                upsert_post(post)
                generated_count += 1
                
        time.sleep(2)
    
    print(f"\nGenerated {generated_count} infographics")

if __name__ == "__main__":
    main()
