#!/usr/bin/env python3
"""
LLM Lens - End-to-End System Test
Tests the complete pipeline from DB to Dashboard APIs.
"""
import json
import sys
import requests
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from db_client import get_recent_posts, init_db

def test_database():
    """Test database connectivity and data integrity."""
    print("\n=== Testing Database ===")
    try:
        posts = get_recent_posts(10)
        print(f"✓ Database connected: Found {len(posts)} posts")
        
        if posts:
            sample = posts[0]
            print(f"✓ Sample post: {sample['headline'][:50]}...")
            print(f"  - Has visual: {bool(sample['visual_path'])}")
            print(f"  - Has full_content: {bool(sample['full_content'])}")
            return True
        else:
            print("⚠ Database is empty - run manual_sync.py first")
            return False
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_feed_api():
    """Test the /api/feed endpoint."""
    print("\n=== Testing Feed API ===")
    try:
        response = requests.get("http://localhost:3000/api/feed", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Feed API responding: {len(data)} items")
            if data:
                item = data[0]
                print(f"  - Title: {item.get('title', 'N/A')[:50]}...")
                print(f"  - Image: {item.get('image_url', 'None')}")
                print(f"  - Has full_content: {bool(item.get('full_content'))}")
            return True
        else:
            print(f"✗ Feed API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to localhost:3000 - is npm run dev running?")
        return False
    except Exception as e:
        print(f"✗ Feed API error: {e}")
        return False

def test_chat_api():
    """Test the /api/chat endpoint."""
    print("\n=== Testing Chat API ===")
    try:
        # Get a post ID from the DB
        posts = get_recent_posts(1)
        if not posts:
            print("⚠ No posts in database to test chat")
            return False
        
        post_id = posts[0]['id']
        payload = {
            "postId": post_id,
            "messages": [{"role": "user", "content": "What are the key takeaways?"}]
        }
        
        response = requests.post(
            "http://localhost:3000/api/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Chat API responding")
            print(f"  - Response: {data.get('content', 'N/A')[:100]}...")
            return True
        else:
            print(f"✗ Chat API returned status {response.status_code}")
            print(f"  - Error: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to localhost:3000")
        return False
    except Exception as e:
        print(f"✗ Chat API error: {e}")
        return False

def test_visual_generation():
    """Test visual generation capability."""
    print("\n=== Testing Visual Generation ===")
    feed_dir = Path("web/public/feed")
    if not feed_dir.exists():
        print("✗ Feed directory does not exist")
        return False
    
    images = list(feed_dir.glob("*.png")) + list(feed_dir.glob("*.jpg"))
    print(f"✓ Found {len(images)} visual(s) in feed directory")
    
    if images:
        for img in images[:3]:
            print(f"  - {img.name}")
    
    return len(images) > 0

def main():
    print("╔═══════════════════════════════════════════╗")
    print("║   LLM LENS - System Integration Test     ║")
    print("╚═══════════════════════════════════════════╝")
    
    results = {
        "Database": test_database(),
        "Feed API": test_feed_api(),
        "Chat API": test_chat_api(),
        "Visuals": test_visual_generation()
    }
    
    print("\n" + "="*45)
    print("RESULTS:")
    passed = sum(results.values())
    total = len(results)
    
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {test}")
    
    print(f"\nFinal Score: {passed}/{total} tests passed")
    print("="*45)
    
    if passed == total:
        print("\n🎉 All systems operational! Dashboard ready.")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Check logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
