# 40_create_visual.md

**Goal:** Generate high-resolution, mobile-friendly infographics using the Nano Banana Pro API based on distilled facts.

**Inputs:**
- Fact JSONs in `.tmp/facts/`

**Tools:**
- `execution/create_visual.py`
- Nano Banana Pro API (via `google-genai` or specific client)

**Outputs:**
- Images in `web/public/feed/` (e.g. `title_hash.png`)
- Metadata JSON linking facts to image.

**Process:**
1. Read facts.
2. Generate an "Art Direction" prompt (style: modern, glassmorphism, dark mode).
3. Call Image Gen API.
4. (Optional) Run OCR/Critique to verify text readability.
5. Save image.

**Styles:**
- Dynamic, neon accents, dark background.
- Clear typography.
- "Bento box" layouts for stats.
