import feedparser
import requests
from datetime import datetime, timedelta

RSS_FEEDS = [
    {
        "name": "MIT Tech Review AI",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed"
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/"
    }
]

def test_feeds():
    for f in RSS_FEEDS:
        print(f"Testing {f['name']}...")
        try:
            # First check if the URL is even reachable
            r = requests.get(f['url'], timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            print(f"  HTTP Status: {r.status_code}")
            
            feed = feedparser.parse(f['url'])
            if feed.bozo:
                print(f"  BOZO Warning: {feed.bozo_exception}")
            
            print(f"  Title: {feed.feed.get('title', 'N/A')}")
            print(f"  Entries found: {len(feed.entries)}")
            
            if len(feed.entries) > 0:
                print(f"  Latest entry date: {feed.entries[0].get('published', 'N/A')}")
                print(f"  Latest entry title: {feed.entries[0].get('title', 'N/A')}")
        except Exception as e:
            print(f"  Error: {e}")
        print("-" * 40)

if __name__ == "__main__":
    test_feeds()
