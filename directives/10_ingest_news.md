# 10_ingest_news.md

**Goal:** Fetch latest AI, LLM, and Tech news from configured RSS feeds and save them for processing.

**Inputs:**
- RSS Feeds (configured in script or .env)
  - TechCrunch AI
  - VentureBeat AI
  - MIT Technology Review
  - The Verge AI
- Reddit (via API/scraping)
  - r/MachineLearning (hot + top of week)
  - r/artificial
  - r/OpenAI
  - r/LocalLLaMA
- Time Filter: Last 7 days only

**Tools:**
- `execution/ingest_news.py`

**Outputs:**
- JSON files in `.tmp/raw_news/` containing:
  - Title
  - Link
  - Published Date
  - Summary/Content
  - Source Name

**Edge Cases:**
- Network timeout: Retry 3 times.
- Malformed RSS: Skip and log warning.
- Duplicate entries: Dedup based on URL.
- Reddit rate limits: Use PRAW with proper delays.
