#!/usr/bin/env python3
import os
import json
from uuid import uuid4
from datetime import datetime

# Create test article that will definitely pass relevance
test_article = {
    "id": str(uuid4()),
    "title": "OpenAI Announces GPT-5: 10x Faster with Multimodal Reasoning",
    "link": "https://example.com/gpt5-announcement",
    "published": datetime.now().isoformat(),
    "summary": "OpenAI today unveiled GPT-5, featuring groundbreaking improvements in speed and multimodal capabilities. The new model processes 10 million tokens per second, 10x faster than GPT-4, and demonstrates advanced reasoning across text, images, and audio simultaneously. The release includes a new architecture that reduces inference costs by 50% while maintaining state-of-the-art performance across all benchmarks.",
    "source": "AI News",
    "fetched_at": datetime.now().isoformat(),
    "analysis": {
        "relevance_score": 10,
        "category": "Model Release",
        "infographic_worthy": True,
        "reasoning": "Major model release from leading AI lab with significant performance improvements"
    },
    "facts": {
        "headline": "GPT-5: 10x Faster Multimodal AI",
        "key_stats": ["10M tokens/sec", "10x faster than GPT-4", "50% cost reduction"],
        "entities": ["OpenAI", "GPT-5"],
        "simple_explanation": "OpenAI's new GPT-5 model is 10 times faster than its predecessor and can understand text, images, and audio together, while costing half as much to run.",
        "visual_concepts": [
            "Speed comparison bar chart: GPT-4 vs GPT-5",
            "Cost reduction visualization",
            "Multimodal capabilities diagram"
        ]
    }
}

# Save to filtered news
filtered_dir = os.path.join(os.getcwd(), '.tmp', 'filtered_news')
os.makedirs(filtered_dir, exist_ok=True)

filepath = os.path.join(filtered_dir, f"test_gpt5_{test_article['id'][:8]}.json")
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(test_article, f, indent=2)

print(f"Created test article: {filepath}")

# Also save to facts directory
facts_dir = os.path.join(os.getcwd(), '.tmp', 'facts')
os.makedirs(facts_dir, exist_ok=True)

facts_filepath = os.path.join(facts_dir, f"test_gpt5_{test_article['id'][:8]}.json")
with open(facts_filepath, 'w', encoding='utf-8') as f:
    json.dump(test_article, f, indent=2)

print(f"Created test facts: {facts_filepath}")
print("\nNow run:")
print("  python execution/create_visual.py")
print("  python execution/sync_feed.py")
