#!/usr/bin/env python3
import os
import json
import time
import feedparser
import requests
from datetime import datetime, timedelta
from uuid import uuid4
import database  # Import the new DB module

# Configuration
RSS_FEEDS = [
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/"
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/"
    },
    {
        "name": "MIT Tech Review AI",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed"
    },
    {
        "name": "Wired AI",
        "url": "https://www.wired.com/feed/tag/ai/latest/rss"
    },
    {
        "name": "Guardian AI",
        "url": "https://www.theguardian.com/technology/artificialintelligenceai/rss"
    },
    {
        "name": "The Verge - AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
    },
    {
        "name": "ArXiv CS.AI",
        "url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=lastUpdatedDate&sortOrder=descending&max_results=10",
        "limit": 5  # Only take top 5 papers per run
    }
]

REDDIT_SUBS = [
    {"name": "r/MachineLearning", "sub": "MachineLearning", "filter": "hot"},
    {"name": "r/artificial", "sub": "artificial", "filter": "hot"},
    {"name": "r/OpenAI", "sub": "OpenAI", "filter": "hot"},
    {"name": "r/LocalLLaMA", "sub": "LocalLLaMA", "filter": "hot"},
]

TIME_FILTER_DAYS = 7  # Only news from last 7 days

def ensure_output_dir():
    # Deprecated: DB handles storage
    pass

def is_recent(date_str, days=TIME_FILTER_DAYS):
    """Check if date is within last N days"""
    try:
        if isinstance(date_str, str):
            # Parse various date formats
            from dateutil import parser
            pub_date = parser.parse(date_str)
        else:
            pub_date = datetime.now()
        
        cutoff = datetime.now() - timedelta(days=days)
        return pub_date.replace(tzinfo=None) >= cutoff.replace(tzinfo=None)
    except:
        # If can't parse, assume it's recent
        return True

def fetch_feed(feed_config):
    print(f"Fetching {feed_config['name']}...")
    try:
        feed = feedparser.parse(feed_config['url'])
        if feed.bozo:
             print(f"Warning: Issue parsing {feed_config['name']}: {feed.bozo_exception}")
        
        # Filter for recent entries only
        recent_entries = [e for e in feed.entries if is_recent(e.get('published', ''))]
        print(f"  Found {len(recent_entries)} recent entries (last {TIME_FILTER_DAYS} days)")
        return recent_entries
    except Exception as e:
        print(f"Error fetching {feed_config['name']}: {e}")
        return []

def fetch_reddit(sub_config):
    """Fetch Reddit posts using JSON API (no auth needed for public posts)"""
    print(f"Fetching {sub_config['name']}...")
    try:
        url = f"https://www.reddit.com/r/{sub_config['sub']}/{sub_config['filter']}.json?limit=25"
        headers = {'User-Agent': 'LLMLens/1.0'}
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            posts = []
            
            for post in data['data']['children']:
                p = post['data']
                # Filter for recent and AI-related
                created = datetime.fromtimestamp(p['created_utc'])
                if is_recent(created.isoformat()):
                    posts.append({
                        'title': p['title'],
                        'link': f"https://reddit.com{p['permalink']}",
                        'published': created.isoformat(),
                        'summary': p.get('selftext', '')[:2000] if p.get('selftext') else p['title'],
                        'score': p['score'],
                        'comments': p['num_comments']
                    })
            
            print(f"  Found {len(posts)} recent posts")
            return posts, sub_config['name']
        else:
            print(f"  Failed: HTTP {response.status_code}")
            return [], sub_config['name']
    except Exception as e:
        print(f"Error fetching {sub_config['name']}: {e}")
        return [], sub_config['name']

def save_entry(entry, source_name):
    data = {
        "id": str(uuid4()),
        "title": entry.get('title', 'No Title'),
        "link": entry.get('link', ''),
        "published": entry.get('published', datetime.now().isoformat()),
        "summary": entry.get('summary', ''),
        "source": source_name,
        "fetched_at": datetime.now().isoformat()
    }
    
    # Add Reddit-specific metadata if present
    if 'score' in entry:
        data['reddit_score'] = entry['score']
        data['reddit_comments'] = entry.get('comments', 0)
    
    # Save to database
    success = database.insert_article(data)
    return success

def main():
    database.init_db()  # Ensure DB is ready
    print(f"Starting News Ingestion (last {TIME_FILTER_DAYS} days)...")
    print("=" * 60)
    
    total_saved = 0
    
    # Fetch RSS feeds
    print("\n[RSS FEEDS]:")
    for feed_config in RSS_FEEDS:
        entries = fetch_feed(feed_config)
        
        # Apply limit if it exists (e.g., for ArXiv)
        if "limit" in feed_config:
            print(f"  Filtering to top {feed_config['limit']} entries (Quality Control)")
            entries = entries[:feed_config['limit']]

        for entry in entries:
            if save_entry(entry, feed_config['name']):
                total_saved += 1
        time.sleep(1)  # Be polite
    
    # Fetch Reddit
    print("\n[REDDIT]:")
    for sub_config in REDDIT_SUBS:
        posts, source = fetch_reddit(sub_config)
        for post in posts:
            if save_entry(post, source):
                total_saved += 1
        time.sleep(2)  # Reddit rate limit politeness
    
    print("=" * 60)
    print(f"[SUCCESS] Ingestion complete. Saved {total_saved} new articles to database.")

if __name__ == "__main__":
    main()
