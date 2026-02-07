#!/usr/bin/env python3
"""Generate placeholder visuals for all posts missing infographics."""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

sys.path.append(str(Path(__file__).parent))
from db_client import get_pending_visuals, upsert_post

def create_infographic(post, output_path):
    """Create a placeholder infographic for a post."""
    width, height = 1200, 1600
    img = Image.new('RGB', (width, height), color='#0a0a1a')
    draw = ImageDraw.Draw(img)
    
    # Parse metadata
    metadata = post.get('metadata')
    if isinstance(metadata, str):
        metadata = json.loads(metadata)
    
    facts = metadata.get('facts', {})
    key_stats = facts.get('key_stats', [])
    
    # Draw gradient background
    for y in range(height):
        opacity = int(255 * (y / height))
        color = (10 + opacity // 10, 10 + opacity // 20, 26 + opacity // 5)
        draw.rectangle([(0, y), (width, y + 1)], fill=color)
    
    # Draw glow circles
    for i in range(3):
        x = width // 4 * (i + 1)
        y = height // 3
        for radius in range(200, 10, -10):
            opacity = int(255 * (200 - radius) / 190)
            color = (100, 150 + opacity // 5, 255, opacity)
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], 
                        outline=color, width=2)
    
    # Load fonts
    try:
        font_large = ImageFont.truetype("arial.ttf", 100)
        font_medium = ImageFont.truetype("arial.ttf", 50)
        font_small = ImageFont.truetype("arial.ttf", 35)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title (split into lines if too long)
    title = post['headline']
    words = title.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if len(test_line) > 25:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw title lines
    y_pos = 150
    for line in lines[:3]:  # Max 3 lines
        draw.text((width // 2, y_pos), line, fill='#00d4ff', anchor="mm", font=font_medium)
        y_pos += 80
    
    # Draw source
    draw.text((width // 2, y_pos + 50), f"Source: {post['source']}", 
             fill='#888', anchor="mm", font=font_small)
    
    # Draw stats
    y_start = 650
    for i, stat in enumerate(key_stats[:3]):
        y = y_start + i * 250
        draw.rectangle([100, y - 70, width - 100, y + 130], 
                      outline='#00d4ff', width=4, fill='#1a1a2e')
        
        # Stat value (larger)
        draw.text((width // 2, y), stat, fill='#00ff88', anchor="mm", font=font_large)
    
    # Impact score badge
    score = post.get('impact_score', 50)
    draw.ellipse([width//2 - 100, height - 250, width//2 + 100, height - 50], 
                fill='#1a1a2e', outline='#00d4ff', width=5)
    draw.text((width // 2, height - 150), f"{score}", fill='#00ff88', anchor="mm", font=font_large)
    draw.text((width // 2, height - 80), "Impact", fill='#888', anchor="mm", font=font_small)
    
    img.save(output_path)
    return True

def main():
    output_dir = Path('web/public/feed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pending = get_pending_visuals(limit=10)
    print(f"Found {len(pending)} posts needing visuals...")
    
    generated = 0
    for post in pending:
        safe_title = "".join([c if c.isalnum() else "_" for c in post['headline'] or 'post'])[:30]
        filename = f"{safe_title}_{post['id'][:8]}.png"
        output_path = output_dir / filename
        
        print(f"Generating: {post['headline'][:50]}...")
        
        if create_infographic(post, str(output_path)):
            post['visual_path'] = f"/feed/{filename}"
            upsert_post(post)
            generated += 1
            print(f"  ✓ Saved: {filename}")
    
    print(f"\n✅ Generated {generated} infographics")

if __name__ == "__main__":
    main()
