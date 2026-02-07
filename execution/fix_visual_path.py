#!/usr/bin/env python3
"""Fix the visual path for existing post and verify."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from db_client import get_recent_posts, upsert_post

# Get the post
posts = get_recent_posts(10)
if posts:
    post = posts[0]
    print(f"Current post: {post['headline']}")
    print(f"Current visual_path: {post['visual_path']}")
    
    # Update with correct path
    post['visual_path'] = '/feed/GPT_5_10x_Faster_Mul_a1b1b6f7.png'
    upsert_post(post)
    
    print(f"Updated visual_path to: {post['visual_path']}")
    
    # Verify
    updated = get_recent_posts(1)[0]
    print(f"Verified visual_path: {updated['visual_path']}")
else:
    print("No posts found")
