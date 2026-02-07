# Self-Critique Agent (SOP)

## Purpose
Verifies the quality, readability, and factual accuracy of generated infographics using vision-language models.

## Workflow

### 1. Vision Analysis
- Input: Generated PNG from `web/public/feed/`.
- Tool: Gemini 3 Pro (Vision).
- Action: Perform OCR and visual layout analysis.

### 2. Validation Criteria
- **Readability**: Is the text clear and not garbled?
- **Factual Accuracy**: Does the text in the image match the source facts (Stats, Names)?
- **Clarity**: Is information presented logically?
- **Aesthetics**: Is the visual style consistent with "LLM Lens" (Futurist, High-Tech)?

### 3. Decision Matrix
- **Score (0-10)**:
  - 8-10: **PASS**. No changes needed.
  - 5-7: **WARN**. Minor issues, maybe mark for human review or proceed.
  - <5: **FAIL**. Trigger regeneration of visual or summary.

## Tooling
- `execution/self_critique.py`
- Model: `gemini-3-pro-preview` (multimodal)
