# 20_analyze_relevance.md

**Goal:** Analyze raw news items to determine if they are relevant to AI/LLMs/Hardware and "infographic worthy".

**Inputs:**
- Raw news JSONs in `.tmp/raw_news/`

**Tools:**
- `execution/analyze_relevance.py`
- Google Gemini API (model: `gemini-1.5-pro` or similar)

**Outputs:**
- Filtered news JSONs in `.tmp/filtered_news/`
- Each file should include:
  - Original data
  - Relevance Score (0-10)
  - Category (Model Release, Chip Advancement, Industry Shift, Application, Other)
  - Reasoning (Why is it worthy?)

**Criteria for Infographic Worthy:**
- High Impact (Major release, breakthrough, big funding)
- Data-rich (Contains numbers, benchmarks, comparisons)
- Visual Logic (Can be visualized as a chart, timeline, or diagram)

**Edge Cases:**
- API Rate Limit: Backoff and retry.
- Content too short: Skip.
