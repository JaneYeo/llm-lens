#!/usr/bin/env python3
"""
Professional Infographic Generator - Production Quality
Based on modern design best practices and user-provided examples.

Design Principles Applied:
- Clean, minimalist layouts with proper white space
- Strategic use of icons (not decorative)
- Clear visual hierarchy
- Professional typography
- Purposeful color schemes
- Data-driven storytelling
"""
import os
import sys
import json
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.append(str(Path(__file__).parent))
from db_client import get_pending_visuals, upsert_post

# Color palettes for different categories
CATEGORY_COLORS = {
    "Technology": {"primary": "#2563EB", "secondary": "#60A5FA", "accent": "#DBEAFE"},  # Blue
    "Business": {"primary": "#7C3AED", "secondary": "#A78BFA", "accent": "#EDE9FE"},  # Purple
    "Science": {"primary": "#059669", "secondary": "#34D399", "accent": "#D1FAE5"},  # Green
    "Health": {"primary": "#DC2626", "secondary": "#F87171", "accent": "#FEE2E2"},  # Red
    "Finance": {"primary": "#EA580C", "secondary": "#FB923C", "accent": "#FED7AA"},  # Orange
    "AI": {"primary": "#0891B2", "secondary": "#06B6D4", "accent": "#CFFAFE"},  # Cyan
    "General": {"primary": "#4B5563", "secondary": "#9CA3AF", "accent": "#F3F4F6"},  # Gray
}

def get_category_colors(category):
    """Get color scheme for a category."""
    for key in CATEGORY_COLORS:
        if key.lower() in category.lower():
            return CATEGORY_COLORS[key]
    return CATEGORY_COLORS["General"]

def create_minimal_infographic(post, output_path):
    """
    Create a clean, professional infographic inspired by examples.
    
    Layout Style: Clean data visualization with clear hierarchy
    """
    width, height = 1200, 1600
    
    # Parse post data
    headline = post.get('headline', 'News Update')
    summary = post.get('summary', '')
    source = post.get('source', 'Unknown')
    impact_score = post.get('impact_score', 75)
    
    metadata = post.get('metadata')
    if isinstance(metadata, str):
        metadata = json.loads(metadata)
    
    facts = metadata.get('facts', {})
    key_stats = facts.get('key_stats', [])
    category = metadata.get('analysis', {}).get('category', 'General')
    colors = get_category_colors(category)
    
    # Create clean white background
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 58)
        font_subtitle = ImageFont.truetype("arial.ttf", 32)
        font_stat = ImageFont.truetype("arialbd.ttf", 72)
        font_label = ImageFont.truetype("arial.ttf", 28)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_title = font_subtitle = font_stat = font_label = font_small = ImageFont.load_default()
    
    # === HEADER SECTION ===
    # Category tag at top
    cat_text = category.upper()
    cat_bbox = draw.textbbox((0, 0), cat_text, font=font_small)
    cat_width = cat_bbox[2] - cat_bbox[0]
    draw.rectangle([60, 60, 60 + cat_width + 40, 110], 
                   fill=colors['primary'])
    draw.text((80, 85), cat_text, fill='#FFFFFF', anchor="lm", font=font_small)
    
    # === TITLE SECTION === 
    # Clean title with proper line breaking
    words = headline.split()
    lines = []
    current_line = []
    max_width = width - 120  # Margins
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_title)
        if bbox[2] - bbox[0] > max_width and current_line:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw title lines
    y_pos = 180
    for line in lines[:4]:  # Max 4 lines
        draw.text((60, y_pos), line, fill='#111827', anchor="lm", font=font_title)
        y_pos += 75
    
    # Source attribution
    draw.text((60, y_pos + 20), f"Source: {source}", 
             fill='#6B7280', anchor="lm", font=font_label)
    
    # Horizontal divider
    y_pos += 90
    draw.rectangle([60, y_pos, width - 60, y_pos + 3], fill=colors['accent'])
    
    # === KEY STATS SECTION ===
    y_pos += 60
    
    if key_stats and len(key_stats) > 0:
        # Title for this section
        draw.text((60, y_pos), "KEY INSIGHTS", fill='#374151', 
                 anchor="lm", font=font_label)
        y_pos += 60
        
        # Display up to 3 stats in clean cards
        for i, stat in enumerate(key_stats[:3]):
            if not stat:
                continue
            
            card_y = y_pos + i * 240
            card_height = 200
            
            # Card background (light, clean)
            draw.rounded_rectangle(
                [80, card_y, width - 80, card_y + card_height],
                radius=16, 
                fill=colors['accent'],
                outline=colors['secondary'],
                width=3
            )
            
            # Stat value (large, bold, centered)
            stat_bbox = draw.textbbox((0, 0), stat, font=font_stat)
            stat_width = stat_bbox[2] - stat_bbox[0]
            stat_x = (width - stat_width) // 2
            
            draw.text((stat_x, card_y + card_height // 2), stat, 
                     fill=colors['primary'], anchor="lm", font=font_stat)
            
            # Small icon indicator (circle)
            circle_r = 12
            draw.ellipse([100, card_y + 30, 100 + circle_r*2, card_y + 30 + circle_r*2],
                        fill=colors['secondary'])
    else:
        # If no stats, show summary
        draw.text((60, y_pos), "SUMMARY", fill='#374151', 
                 anchor="lm", font=font_label)
        y_pos += 60
        
        # Word wrap summary
        summary_words = summary[:200].split()  # Limit length
        summary_lines = []
        current = []
        
        for word in summary_words:
            test = ' '.join(current + [word])
            bbox = draw.textbbox((0, 0), test, font=font_subtitle)
            if bbox[2] - bbox[0] > width - 160:
                if current:
                    summary_lines.append(' '.join(current))
                    current = [word]
            else:
                current.append(word)
        if current:
            summary_lines.append(' '.join(current))
        
        for line in summary_lines[:6]:  # Max 6 lines
            draw.text((80, y_pos), line, fill='#4B5563', 
                     anchor="lm", font=font_subtitle)
            y_pos += 50
    
    # === IMPACT SCORE (Bottom Section) ===
    score_y = height - 300
    
    # Clean progress bar style
    bar_width = width - 160
    bar_height = 40
    bar_x = 80
    
    # Background
    draw.rounded_rectangle([bar_x, score_y, bar_x + bar_width, score_y + bar_height],
                          radius=20, fill='#F3F4F6')
    
    # Filled portion
    fill_width = int((impact_score / 100) * bar_width)
    if fill_width > 0:
        draw.rounded_rectangle([bar_x, score_y, bar_x + fill_width, score_y + bar_height],
                              radius=20, fill=colors['primary'])
    
    # Score text
    score_text = f"{impact_score}% IMPACT SCORE"
    draw.text((width // 2, score_y + 20), score_text, 
             fill='#FFFFFF', anchor="mm", font=font_label)
    
    # Footer branding
    draw.text((width // 2, height - 80), "LLM LENS", 
             fill='#9CA3AF', anchor="mm", font=font_small)
    draw.text((width // 2, height - 50), "Powered by AI Intelligence", 
             fill='#D1D5DB', anchor="mm", font=font_small)
    
    # Save
    img.save(output_path, 'PNG', quality=95)
    return True

def main():
    """Generate professional infographics for all pending posts."""
    output_dir = Path('web/public/feed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Delete old ugly infographics
    old_files = list(output_dir.glob('*.png'))
    print(f"Removing {len(old_files)} old infographics...")
    for f in old_files:
        f.unlink()
    
    # Generate new professional ones
    pending = get_pending_visuals(limit=100)
    print(f"\nGenerating {len(pending)} professional infographics...")
    print("Design: Clean, minimal, data-focused\n")
    
    generated = 0
    for i, post in enumerate(pending, 1):
        safe_title = "".join([c if c.isalnum() else "_" for c in post['headline']])[:30]
        filename = f"{safe_title}_{post['id'][:8]}.png"
        output_path = output_dir / filename
        
        if i <= 10 or i % 10 == 0:
            print(f"[{i}/{len(pending)}] {post['headline'][:55]}...")
        
        if create_minimal_infographic(post, str(output_path)):
            post['visual_path'] = f"/feed/{filename}"
            upsert_post(post)
            generated += 1
    
    print(f"\n✅ Generated {generated} professional infographics")
    print("   Design: Modern, clean, professional")
    print("   Features: Strategic color use, clear hierarchy, proper white space")

if __name__ == "__main__":
    main()
