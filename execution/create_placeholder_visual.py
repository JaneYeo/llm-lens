#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

# Create a simple infographic placeholder
width, height = 1200, 1600
img = Image.new('RGB', (width, height), color='#0a0a1a')
draw = ImageDraw.Draw(img)

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

# Draw text
try:
    font_large = ImageFont.truetype("arial.ttf", 120)
    font_medium = ImageFont.truetype("arial.ttf", 60)
    font_small = ImageFont.truetype("arial.ttf", 40)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Title
draw.text((width // 2, 200), "GPT-5", fill='#00d4ff', anchor="mm", font=font_large)
draw.text((width // 2, 350), "10x Faster", fill='#a855f7', anchor="mm", font=font_medium)
draw.text((width // 2, 450), "Multimodal AI", fill='#ffffff', anchor="mm", font=font_medium)

# Stats
stats = [
    ("Processing Speed", "10x Boost"),
    ("Model Size", "500B Params"),
    ("Latency", "< 100ms")
]

y_start = 700
for i, (label, value) in enumerate(stats):
    y = y_start + i * 200
    draw.rectangle([100, y - 50, width - 100, y + 100], 
                  outline='#00d4ff', width=3, fill='#1a1a2e')
    draw.text((120, y), label, fill='#888', anchor="lm", font=font_small)
    draw.text((width - 120, y), value, fill='#00ff88', anchor="rm", font=font_medium)

# Save
output_path = os.path.join('web', 'public', 'feed', 'GPT_5_10x_Faster_Mul_a1b1b6f7.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
img.save(output_path)
print(f"Created placeholder infographic: {output_path}")
