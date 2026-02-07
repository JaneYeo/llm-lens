#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import database
from datetime import datetime
from uuid import uuid4

# Fix Windows console encoding
import sys
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def seed_article():
    database.init_db()
    
    test_article = {
        "id": str(uuid4()),
        "title": "Google DeepMind Announces 'Gemini Infinite': Real-time World Simulation at Scale",
        "link": "https://deepmind.google/technologies/gemini/infinite",
        "source": "DeepMind Blog",
        "published": datetime.now().isoformat(),
        "summary": "Google DeepMind has revealed Gemini Infinite, a new class of multimodal model capable of simulating complex real-world physics and social dynamics in real-time. The model features an infinite context window managed by 'Neural Memory compressions' and achieves 99.9% accuracy on the new 'WorldSim' benchmark. Sundar Pichai called it 'the final bridge between digital and physical intelligence'.",
        "fetched_at": datetime.now().isoformat()
    }
    
    # Insert directly with 'ingested' status
    if database.insert_article(test_article):
        print(f"Successfully seeded test article: {test_article['title']}")
        print(f"ID: {test_article['id']}")
    else:
        print("Failed to seed article (likely duplicate URL).")

if __name__ == "__main__":
    seed_article()
