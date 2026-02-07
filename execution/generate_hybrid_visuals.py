#!/usr/bin/env python3
"""
Hybrid Infographic Generator - Nano Banana Pro + Fallback
Uses real AI image generation when API key is available, fallback to professional PIL otherwise.
"""
import os
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).parent))
from db_client import get_pending_visuals, upsert_post

# Check for API key
API_KEY = os.getenv('GEMINI_API_KEY')
USE_AI_GENERATION = bool(API_KEY)

if USE_AI_GENERATION:
    client = genai.Client(api_key=API_KEY)
    print("✓ Nano Banana Pro enabled (API key found)")
else:
    print("⚠ No API key - using professional PIL fallback")

# Category colors
CATEGORY_COLORS = {
    "Technology": {"primary": "#2563EB", "secondary": "#60A5FA", "accent": "#DBEAFE"},
    "Business": {"primary": "#7C3AED", "secondary": "#A78BFA", "accent": "#EDE9FE"},
    "Science": {"primary": "#059669", "secondary": "#34D399", "accent": "#D1FAE5"},
    "Health": {"primary": "#DC2626", "secondary": "#F87171", "accent": "#FEE2E2"},
    "Finance": {"primary": "#EA580C", "secondary": "#FB923C", "accent": "#FED7AA"},
    "AI": {"primary": "#0891B2", "secondary": "#06B6D4", "accent": "#CFFAFE"},
    "General": {"primary": "#4B5563", "secondary": "#9CA3AF", "accent": "#F3F4F6"},
}

def get_category_colors(category):
    for key in CATEGORY_COLORS:
        if key.lower() in category.lower():
            return CATEGORY_COLORS[key]
    return CATEGORY_COLORS["General"]

def distill_text(text, target_label):
    """Semi-intelligent extraction from long abstracts if no model available."""
    if not text: return "Data missing."
    lines = text.split('.')
    if target_label == "PROBLEM":
        # Look for challenge words
        for line in lines:
            if any(w in line.lower() for w in ['challenge', 'problem', 'address', 'motivation', 'disparity']):
                return line.strip() + "."
        return lines[0].strip() + "."
    elif target_label == "SOLUTION":
        for line in lines:
            if any(w in line.lower() for w in ['evaluate', 'analyze', 'propose', 'strategies', 'solution', 'objective']):
                return line.strip() + "."
        return "Implementing optimized architectural solutions."
    elif target_label == "IMPACT":
        for line in lines:
            if any(w in line.lower() for w in ['result', 'reveal', 'demonstrate', 'gain', 'improvement', 'correlation']):
                return line.strip() + "."
        return "Significant performance gains and architectural robustness."
    return text[:200] + "..."

def create_ai_prompt(post):
    """Generate high-fidelity MAXIMALIST futuristic HUD prompt using 'baoyu-infographic' framework."""
    headline = post.get('headline', 'Intelligence Briefing')
    summary = post.get('summary', '')
    
    metadata = post.get('metadata')
    if isinstance(metadata, str):
        metadata = json.loads(metadata)
    
    facts = metadata.get('facts', {})
    key_stats = facts.get('key_stats', [])
    
    # Distill content for the prompt to avoid overflow in the image text
    problem_distilled = distill_text(summary, "PROBLEM")
    solution_distilled = distill_text(summary, "SOLUTION")
    impact_distilled = distill_text(summary, "IMPACT")
    
    prompt = f"""### INFOGRAPHIC TASK: STUNNING MAXIMALIST HIGH-TECH HUD ###

Topic: {headline}
Layout: bridge (Problem -> Solution -> Impact)
Style: high-fidelity-hud (NOT minimalist, NOT white)
Aspect: 4:5 Portrait
Language: English

## INFORMATION ARCHITECTURE (Distilled Knowledge)
1. **Title**: Large glowing neon headline: "{headline}"
2. **PHASE 1 (THE PROBLEM)**: "{problem_distilled}"
3. **PHASE 2 (THE IDEA/SOLUTION)**: "{solution_distilled}"
4. **PHASE 3 (THE IMPACT)**: "{impact_distilled}"
5. **METRICS**: "{', '.join(key_stats[:3]) if key_stats else '99.9% Reliability, 10x Performance'}"

## AESTHETIC ENFORCEMENT (MAXIMALIST)
- **THEME**: Deep Dark Mission Control HUD. NO WHITE BACKGROUNDS.
- **BACKGROUND**: Metallic Obsidian with layers of digital blueprints, hexagonal grids, and faint starfields.
- **ACCENTS**: Neon Cyan, Electric Purple, and Hot Amber highlights.
- **ELEMENTS**: High-density tactical UI widgets, spinning orbital rings, 3D wireframe models, data streams, digital pulse waves, and scanlines.
- **LAYOUT**: Feature-rich and immersive. Every corner should have tactical detail (coordinates, status bars, miniature graphs).
- **VIBE**: Advanced Alien/Future Tech Interface. High-fidelity glassmorphism and depth.

## STRICT REQUIREMENTS
- **NO MINIMALISM**: This must be a rich, complex visual experience.
- **NO ABSOLUTE WHITE**: The primary theme is Dark Mode HUD.
- **NO ACADEMIC TEXT**: Use the distilled bullet points provided above.
- **STUNNING FIDELITY**: Professional digital art look.

GENERATE THE MOST HIGH-TECH INFOGRAPHIC POSSIBLE."""
    
    return prompt

def generate_with_ai(post, output_path):
    """Generate infographic using Imagen."""
    try:
        prompt = create_ai_prompt(post)
        
        # Using a more standard Imagen model name if nano-banana-pro fails
        response = client.models.generate_images(
            model="imagen-3.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type="image/png"
            )
        )
        
        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            with open(output_path, 'wb') as f:
                f.write(image_data)
            return True
        return False
    except Exception as e:
        print(f"  AI generation error: {e}")
        return False

def generate_with_pil(post, output_path):
    """Fallback: MAXIMALIST High-Fidelity Futuristic HUD with PIL."""
    width, height = 1200, 1600
    headline = post.get('headline', 'Intelligence Briefing')
    summary = post.get('summary', '')
    impact_score = post.get('impact_score', 85)
    
    metadata = post.get('metadata')
    if isinstance(metadata, str):
        metadata = json.loads(metadata)
    
    facts = metadata.get('facts', {})
    key_stats = facts.get('key_stats', [])
    category = metadata.get('analysis', {}).get('category', 'General')
    colors = get_category_colors(category)
    
    # Deep Maximalist Background
    img = Image.new('RGB', (width, height), '#020406')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 64)
        font_section = ImageFont.truetype("arialbd.ttf", 40)
        font_body = ImageFont.truetype("arial.ttf", 32)
        font_stat = ImageFont.truetype("arialbd.ttf", 80)
        font_small = ImageFont.truetype("arial.ttf", 22)
    except:
        font_title = font_section = font_body = font_stat = font_small = ImageFont.load_default()
    
    # 1. Hexagonal Grid Background (Mock)
    hex_size = 60
    for y in range(0, height, int(hex_size * 1.5)):
        for x in range(0, width, int(hex_size * 1.73)):
            offset = 0 if (y // int(hex_size * 1.5)) % 2 == 0 else int(hex_size * 0.86)
            draw.regular_polygon((x + offset, y, hex_size), 6, outline='#051018', width=1)

    # 2. Scanning Lines
    for i in range(0, height, 10):
        draw.line([0, i, width, i], fill='#03070A', width=1)
    
    # 3. Complex HUD Frame
    padding = 30
    draw.rectangle([padding, padding, width-padding, height-padding], outline='#0A2030', width=2)
    # Reinforced Corners
    draw.rectangle([padding, padding, padding+50, padding+50], fill=colors['primary'])
    draw.rectangle([width-padding-50, height-padding-50, width-padding, height-padding], fill=colors['secondary'])

    # 4. Data Streams (Fake code/coordinates)
    for i in range(10):
        draw.text((width - 150, 100 + i*30), f"SYS_LOC: 0x{i*123:04X}", fill='#0A2030', font=font_small)
        draw.text((50, height - 150 - i*30), f"LOG_STRM: {i*55}.77", fill='#0A2030', font=font_small)

    # 5. Distilled Content Logic
    pb = distill_text(summary, "PROBLEM")
    sl = distill_text(summary, "SOLUTION")
    im = distill_text(summary, "IMPACT")

    # 6. Title Section
    draw.text((80, 80), category.upper() + " // TACTICAL_FEED", fill=colors['secondary'], font=font_small)
    
    # Headline wraps
    y_pos = 140
    words = headline.split()
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_title)
        if bbox[2] - bbox[0] > width - 160:
            draw.text((80, y_pos), ' '.join(current_line), fill='#FFFFFF', font=font_title)
            y_pos += 80
            current_line = [word]
        else:
            current_line.append(word)
    draw.text((80, y_pos), ' '.join(current_line), fill='#FFFFFF', font=font_title)
    y_pos += 120

    # 7. Bridge Sections
    sections = [
        {"h": "[ PHASE 1: ANOMALY_DETECTION ]", "c": pb, "clr": colors['primary']},
        {"h": "[ PHASE 2: STRATEGIC_SOLUTION ]", "c": sl, "clr": "#FACC15"}, # Gold accent
        {"h": "[ PHASE 3: OPERATIONAL_RESULT ]", "c": im, "clr": colors['secondary']}
    ]

    for s in sections:
        draw.text((100, y_pos), s['h'], fill=s['clr'], font=font_section)
        y_pos += 60
        # Wrap content
        content_words = s['c'].split()
        curr = []
        for word in content_words:
            t = ' '.join(curr + [word])
            b = draw.textbbox((0, 0), t, font=font_body)
            if b[2] - b[0] > width - 240:
                draw.text((120, y_pos), ' '.join(curr), fill='#94A3B8', font=font_body)
                y_pos += 45
                curr = [word]
            else:
                curr.append(word)
        draw.text((120, y_pos), ' '.join(curr), fill='#94A3B8', font=font_body)
        y_pos += 100

    # 8. HUD Widgets (Circular Gauges)
    draw.text((80, y_pos), "CORE_METRICS_DASHBOARD", fill=colors['primary'], font=font_small)
    y_pos += 50
    for i, stat in enumerate(key_stats[:3]):
        cx = 250 + (i * 350)
        draw.ellipse([cx-100, y_pos, cx+100, y_pos+200], outline='#0A2030', width=1)
        draw.arc([cx-90, y_pos+10, cx+90, y_pos+190], start=0, end=270, fill=colors['secondary'], width=4)
        draw.text((cx-40, y_pos+80), stat, fill='#FFFFFF', font=font_small)
    
    # 9. Status Bar & Impact
    sbar_y = height - 100
    draw.rectangle([80, sbar_y, width-80, sbar_y+20], outline=colors['primary'], width=1)
    fw = int((impact_score / 100) * (width - 160))
    draw.rectangle([80, sbar_y, 80+fw, sbar_y+20], fill=colors['secondary'])
    draw.text((80, sbar_y - 40), f"DYNAMIC_IMPACT_SCORE: {impact_score}% // STATUS: NOMINAL", fill='#4ADE80', font=font_small)

    img.save(output_path, 'PNG')
    return True

def main():
    """Generate high-fidelity futuristic infographics."""
    output_dir = Path('web/public/feed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear existing visuals to force regeneration
    for f in output_dir.glob("*.png"):
        try: f.unlink()
        except: pass

    pending = get_pending_visuals(limit=30)
    if not pending:
        print("No pending visuals found in DB.")
        return
        
    print(f"\nREDESIGNING {len(pending)} INFOGRAPHICS...")
    print(f"Style: Futuristic HUD / Dark Mode\n")
    
    for i, post in enumerate(pending, 1):
        safe_title = "".join([c if c.isalnum() else "_" for c in post['headline']])[:30]
        filename = f"{safe_title}_{post['id'][:8]}.png"
        output_path = output_dir / filename
        
        print(f"[{i}/{len(pending)}] {post['headline'][:50]}...")
        
        success = False
        if USE_AI_GENERATION:
            print(f"  Attempting AI Generation (Imagen)...")
            success = generate_with_ai(post, str(output_path))
            if not success:
                print(f"  AI Failed. Falling back to High-Fi PIL Dashboard...")
                success = generate_with_pil(post, str(output_path))
        else:
            success = generate_with_pil(post, str(output_path))
            
        if success:
            post['visual_path'] = f"/feed/{filename}"
            upsert_post(post)
            print("  ✓ SUCCESS")
        else:
            print("  ✗ FAILED")

if __name__ == "__main__":
    main()

