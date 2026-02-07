#!/usr/bin/env python3
"""Create multiple sample news posts with visuals for dashboard demo."""
import sys
import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta

sys.path.append(str(Path(__file__).parent))
from db_client import upsert_post

# Sample news data
SAMPLE_POSTS = [
    {
        "headline": "GPT-5: 10x Faster Multimodal AI",
        "summary": "OpenAI unveils GPT-5 with revolutionary 10x performance boost across text, image, and audio processing.",
        "source": "AI News",
        "impact_score": 95,
        "key_stats": ["10x faster", "500B params", "<100ms latency"]
    },
    {
        "headline": "Quantum Computing Breakthrough at Google",
        "summary": "Google achieves quantum supremacy with new 1000-qubit processor, solving problems in minutes that would take classical computers millennia.",
        "source": "Tech Times",
        "impact_score": 90,
        "key_stats": ["1000 qubits", "99.9% fidelity", "100,000x faster"]
    },
    {
        "headline": "Tesla Unveils Fully Autonomous RoboTaxi Fleet",
        "summary": "Tesla launches commercial self-driving taxi service in 5 major cities, marking the beginning of autonomous transportation era.",
        "source": "Auto World",
        "impact_score": 85,
        "key_stats": ["5 cities", "$0.50/mile", "24/7 service"]
    },
    {
        "headline": "SpaceX Mars Colony: First 1000 Applications Approved",
        "summary": "SpaceX announces selection of first 1000 colonists for Mars settlement program launching in 2028.",
        "source": "Space Daily",
        "impact_score": 92,
        "key_stats": ["1000 colonists", "2028 launch", "$200B investment"]
    },
    {
        "headline": "Medical AI Detects Cancer 5 Years Earlier Than Traditional Methods",
        "summary": "New AI diagnostic tool achieves 99.7% accuracy in early cancer detection, potentially saving millions of lives annually.",
        "source": "Health Tech",
        "impact_score": 88,
        "key_stats": ["99.7% accuracy", "5 years earlier", "40% mortality reduction"]
    }
]

def create_posts():
    created = 0
    base_time = datetime.now()
    
    for i, data in enumerate(SAMPLE_POSTS):
        post_id = str(uuid.uuid4())
        
        # Build full content for chatbot
        full_content = f"""
Headline: {data['headline']}
Source: {data['source']}
Impact Score: {data['impact_score']}/100

Summary: {data['summary']}

Key Statistics:
{chr(10).join(f'- {stat}' for stat in data['key_stats'])}

Analysis:
This development represents a significant milestone in the field. The implications
for industry and society are substantial, with potential to reshape how we approach
this domain. Experts predict widespread adoption within the next 2-3 years.

Investment Potential: High
Risk Level: Medium
Timeline: 2-5 years to mainstream adoption
        """.strip()
        
        # Create metadata
        metadata = {
            "id": post_id,
            "title": data["headline"],
            "source": data["source"],
            "facts": {
                "headline": data["headline"],
                "simple_explanation": data["summary"],
                "key_stats": data["key_stats"]
            },
            "analysis": {
                "relevance_score": data["impact_score"],
                "category": "Technology",
                "infographic_worthy": True
            }
        }
        
        post = {
            "id": post_id,
            "headline": data["headline"],
            "summary": data["summary"],
            "full_content": full_content,
            "impact_score": data["impact_score"],
            "visual_path": None,  # Will be generated separately
            "source": data["source"],
            "created_at": (base_time - timedelta(hours=i*2)).isoformat(),
            "metadata": metadata
        }
        
        upsert_post(post)
        created += 1
        print(f"✓ Created: {data['headline'][:50]}...")
    
    print(f"\n✅ Successfully created {created} sample posts")
    print("Run create_visual.py to generate infographics")

if __name__ == "__main__":
    create_posts()
