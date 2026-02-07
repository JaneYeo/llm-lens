#!/usr/bin/env python3
"""
Generate enhanced placeholder visuals with modern tech aesthetic.
Professional looking infographics without requiring API keys.
"""
import os
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

sys.path.append(str(Path(__file__).parent))
from db_client import get_pending_visuals, upsert_post

def draw_glow_effect(draw, xy, radius, color, intensity=10):
    """Draw a glowing circle effect."""
    x, y = xy
    for i in range(intensity, 0, -1):
        alpha = int(255 * (i / intensity) * 0.3)
        r = radius + (intensity - i) * 3
        glow_color = (*color, alpha)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=glow_color)

def create_professional_infographic(post, output_path):
    """Create a professional, tech-styled infographic."""
    width, height = 1200, 1600
    
    # Parse metadata
    metadata = post.get('metadata')
    if isinstance(metadata, str):
        metadata = json.loads(metadata)
    
    facts = metadata.get('facts', {})
    key_stats = facts.get('key_stats', [])
    category = metadata.get('analysis', {}).get('category', 'Technology')
    
    # Create base image with gradient
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # Draw gradient background
    for y in range(height):
        progress = y / height
        r = int(10 + progress * 16)
        g = int(10 + progress * 16)
        b = int(26 + progress * 24)
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b, 255))
    
    # Add subtle noise texture
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw abstract tech background
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        w = random.randint(50, 200)
        h = random.randint(2, 4)
        opacity = random.randint(10, 40)
        draw.rectangle([x, y, x+w, y+h], fill=(0, 212, 255, opacity))
    
    # Draw glow circles
    glow_colors = [(0, 212, 255), (168, 85, 247), (0, 255, 136)]
    for i in range(3):
        x = width // 4 * (i + 1)
        y = height // 4
        color = glow_colors[i % len(glow_colors)]
        
        for radius in range(150, 20, -10):
            opacity = int((150 - radius) / 130 * 180)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius],
                        outline=(*color, opacity), width=2)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 70)
        font_large = ImageFont.truetype("arialbd.ttf", 90)
        font_medium = ImageFont.truetype("arial.ttf", 45)
        font_small = ImageFont.truetype("arial.ttf", 32)
    except:
        font_title = font_large = font_medium = font_small = ImageFont.load_default()
    
    # Split title into multiple lines
    headline = post.get('headline', 'News Update')
    words = headline.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if len(test_line) > 22:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw title with shadow
    y_pos = 160
    for line in lines[:3]:
        # Shadow
        draw.text((width//2 + 3, y_pos + 3), line, fill=(0, 0, 0, 180), 
                 anchor="mm", font=font_title)
        # Main text with gradient effect
        draw.text((width//2, y_pos), line, fill=(0, 212, 255, 255), 
                 anchor="mm", font=font_title)
        y_pos += 90
    
    # Category badge
    bbox = draw.textbbox((0, 0), category, font=font_small)
    badge_width = bbox[2] - bbox[0] + 40
    badge_x = (width - badge_width) // 2
    badge_y = y_pos + 20
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_width, badge_y + 60],
                          radius=30, fill=(168, 85, 247, 180), outline=(168, 85, 247, 255), width=2)
    draw.text((width//2, badge_y + 30), category, fill=(255, 255, 255, 255),
             anchor="mm", font=font_small)
    
    # Draw key stats in modern cards
    stats_y = badge_y + 120
    card_height = 200
    card_spacing = 30
    
    for i, stat in enumerate(key_stats[:3]):
        if not stat:
            continue
            
        y = stats_y + i * (card_height + card_spacing)
        
        # Card background with glassmorphism
        draw.rounded_rectangle([80, y, width-80, y+card_height],
                              radius=20, fill=(26, 26, 46, 200), 
                              outline=(0, 212, 255, 255), width=3)
        
        # Stat number/value
        draw.text((width//2, y + card_height//2), stat, 
                 fill=(0, 255, 136, 255), anchor="mm", font=font_large)
        
        # Small decorative elements
        for corner in [(100, y+20), (width-100, y+20)]:
            draw.ellipse([corner[0]-8, corner[1]-8, corner[0]+8, corner[1]+8],
                        fill=(0, 212, 255, 180))
    
    # Impact score badge at bottom
    score = post.get('impact_score', 75)
    circle_y = height - 200
    circle_r = 100
    
    # Outer glow
    for r in range(circle_r + 30, circle_r, -2):
        alpha = int((circle_r + 30 - r) / 30 * 100)
        draw.ellipse([width//2-r, circle_y-r, width//2+r, circle_y+r],
                    fill=(168, 85, 247, alpha))
    
    # Main circle
    draw.ellipse([width//2-circle_r, circle_y-circle_r, 
                  width//2+circle_r, circle_y+circle_r],
                fill=(26, 26, 46, 255), outline=(168, 85, 247, 255), width=5)
    
    # Score text
    draw.text((width//2, circle_y - 15), str(score), 
             fill=(0, 255, 136, 255), anchor="mm", font=font_large)
    draw.text((width//2, circle_y + 40), "IMPACT", 
             fill=(136, 136, 136, 255), anchor="mm", font=font_small)
    
    # Source attribution
    source = post.get('source', 'Unknown Source')
    draw.text((width//2, height - 60), f"Source: {source}", 
             fill=(136, 136, 136, 200), anchor="mm", font=font_small)
    
    # Convert to RGB and save
    rgb_img = Image.new('RGB', img.size, (10, 10, 26))
    rgb_img.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
    rgb_img.save(output_path, 'PNG', quality=95)
    return True

def main():
    """Generate enhanced visuals for posts without them."""
    output_dir = Path('web/public/feed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pending = get_pending_visuals(limit=50)
    print(f"Found {len(pending)} posts needing visuals")
    print(f"Generating enhanced placeholder visuals...\n")
    
    generated = 0
    for i, post in enumerate(pending, 1):
        safe_title = "".join([c if c.isalnum() else "_" for c in post['headline']])[:30]
        filename = f"{safe_title}_{post['id'][:8]}.png"
        output_path = output_dir / filename
        
        if output_path.exists():
            print(f"[{i}/{len(pending)}] ⊙ {post['headline'][:50]}... (exists)")
            continue
        
        print(f"[{i}/{len(pending)}] ✓ {post['headline'][:50]}...")
        
        if create_professional_infographic(post, str(output_path)):
            post['visual_path'] = f"/feed/{filename}"
            upsert_post(post)
            generated += 1
    
    print(f"\n✅ Generated {generated} professional infographics")

if __name__ == "__main__":
    main()
