#!/usr/bin/env python3
"""
Generate professional infographics using Nano Banana Pro (Gemini 3 Pro Image).
Uses the generate_content pattern for multimodal image generation.
"""
import os
import sys
import json
import time
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

sys.path.append(str(Path(__file__).parent))
from database import get_articles_by_status, update_article_status

from dotenv import load_dotenv
load_dotenv()

# Initialize Gemini client
API_KEY = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    print("Error: GEMINI_API_KEY or GOOGLE_API_KEY not set")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# Nano Banana Pro is accessed via gemini-3-pro-image-preview
MODEL_ID = "gemini-3-pro-image-preview"

def create_visual_prompt(post):
    """Generate a detailed prompt for Nano Banana Pro image generation."""
    headline = post.get('headline') or post.get('title') or 'News Update'
    
    # Parse facts for key stats
    facts = post.get('facts_json')
    if isinstance(facts, str):
        facts = json.loads(facts)
    elif not facts:
        facts = {}
    
    key_stats = facts.get('key_stats', [])
    stats_text = ', '.join(key_stats[:3]) if key_stats else "key technological metrics"
    
    prompt = f"""Create a modern, professional infographic for: "{headline}"

Style requirements:
- Dark background (#0a0a1a to #1a1a2e gradient)
- Neon blue (#00d4ff) and purple (#a855f7) accents
- Glassmorphism UI elements with transparency
- Modern tech aesthetic with subtle glow effects

Content to display:
- Main headline in large, bold typography
- Key statistics: {stats_text}
- Abstract tech symbols and icons (circuit boards, neural networks, data flow)
- Futuristic geometric shapes and patterns
- Professional data visualization style

Layout:
- Portrait orientation (3:4 ratio)
- Clean, organized composition
- Visual hierarchy with title at top
- Statistics displayed in sleek data cards
- Icon-based visual elements throughout

Make it look premium, high-tech, and visually striking. Use symbols, icons, and abstract representations rather than photographs. Think dashboard interface meets tech keynote presentation."""
    
    return prompt

def generate_infographic(post, output_path):
    """Generate an infographic using Nano Banana Pro pattern."""
    try:
        # Create prompt
        prompt = create_visual_prompt(post)
        print(f"Generated prompt for: {post['title'][:40]}...")
        
        # Call Gemini 3 Pro Image (Nano Banana Pro) using generate_content pattern
        print(f"Calling Nano Banana Pro ({MODEL_ID})...")
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt],
        )
        
        # Extract and save the image
        found_image = False
        for part in response.parts:
            if part.inline_data:
                try:
                    # Save using PIL
                    img = part.as_image()
                    img.save(output_path)
                    print(f"✓ Saved ({MODEL_ID}): {Path(output_path).name}")
                    found_image = True
                    break
                except Exception as save_err:
                    print(f"  Error saving image: {save_err}")
                    # Fallback to raw bytes
                    if hasattr(part.inline_data, 'data'):
                        with open(output_path, "wb") as f:
                            f.write(part.inline_data.data)
                        print(f"✓ Saved (raw bytes): {Path(output_path).name}")
                        found_image = True
                        break
        
        if not found_image:
            print(f"✗ No image found in response parts. Parts: {[type(p) for p in response.parts]}")
            return False
        
        return True
            
    except Exception as e:
        print(f"✗ API Error generating image: {e}")
        return False

def main():
    """Generate infographics for articles without visuals."""
    output_dir = Path('web/public/feed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get articles needing visuals
    pending = get_articles_by_status('distilled', limit=10)
    print(f"Found {len(pending)} articles needing visuals")
    
    generated = 0
    for i, post in enumerate(pending, 1):
        print(f"[{i}/{len(pending)}] Processing: {post['title'][:50]}...")
        
        # Create safe filename
        safe_title = "".join([c if c.isalnum() else "_" for c in post['title']])[:30]
        filename = f"{safe_title}_{post['id'][:8]}.png"
        output_path = output_dir / filename
        
        # Skip if already exists but update status
        if output_path.exists():
            print(f"  ⊙ Already exists, updating status")
            update_article_status(post['id'], 'visualized', {'image_path': f"/feed/{filename}"})
            continue
        
        # Generate
        if generate_infographic(post, str(output_path)):
            update_article_status(post['id'], 'visualized', {'image_path': f"/feed/{filename}"})
            generated += 1
            # Rate limiting / Quota safety for high-res generation
            time.sleep(3)
        
        print()  # Blank line between items
    
    print(f"\n✅ Finished. Generated {generated} new infographics using Nano Banana Pro pattern.")
    print(f"   View them at http://localhost:3000/dashboard")

if __name__ == "__main__":
    main()
