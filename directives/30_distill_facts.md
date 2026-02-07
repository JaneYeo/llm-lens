# 30_distill_facts.md

**Goal:** Extract structured facts, numbers, and key entities from relevant news items to power the infographic generation.

**Inputs:**
- Filtered/Relevant news JSONs in `.tmp/filtered_news/`

**Tools:**
- `execution/distill_facts.py`
- Google Gemini API

**Outputs:**
- Fact JSONs in `.tmp/facts/` containing:
  - Headline (shortened)
  - Key Statistics / Numbers (e.g. "10M tokens", "50% faster")
  - Entities (Companies, People, Models)
  - Timeline / Dates
  - "Visual Concepts" (Suggestions for visual metaphors)

**Edge Cases:**
- No facts found: Flag as "opinion/editorial" and maybe skip visual generation or use huge quote style.
- Conflicting numbers: Note for user review (later feature).
