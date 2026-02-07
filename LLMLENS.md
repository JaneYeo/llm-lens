# LLM Lens – System Overview

## 1. Introduction

LLM Lens is an autonomous AI-driven system designed to transform AI, LLM, and chip industry news into **fact-checked, visually clear infographics**. The system leverages Gemini 3 Pro for reasoning and Nano Banana Pro for high-resolution multimodal visual generation.

The goal is to help developers, students, investors, and tech content creators quickly grasp key AI developments at a glance without sifting through multiple sources.

---

## 2. System Architecture

The system is organized into multiple agents working together in a pipeline:

### 2.1 News Ingestion Agent

* Collects news from trusted sources (RSS feeds, APIs, scraping).
* Filters only AI, LLM, chip, or AI company-related content.

### 2.2 Relevance & Reasoning Agent

* Uses Gemini 3 Pro to determine if the news is **infographic-worthy**.
* Classifies the news type (Model release, Chip advancement, Use case, Industry shift).
* Maintains long-term context with Thought Signatures for continuous understanding.

### 2.3 Fact Distillation Agent

* Extracts key facts, numbers, entities, and timelines.
* Performs initial impact analysis.

### 2.4 Fact Verification Loop

* Cross-checks numbers and claims across multiple sources.
* Assigns confidence scores.
* Flags uncertain data for review or regeneration.

### 2.5 Visual Planning Agent

* Determines the infographic type and layout.
* Chooses visual hierarchy, color scheme, and typography.

### 2.6 Creative Autopilot

* Uses Nano Banana Pro for image generation and Paint-to-Edit corrections.
* Generates high-resolution, mobile-friendly infographics.

### 2.7 Self-Critique Agent

* Performs OCR to read generated images.
* Verifies readability, accuracy, and clarity.
* Regenerates the infographic if issues are detected.

### 2.8 Output Layer

* Publishes the infographic in the feed.
* Optional: Provides Live explanation using Gemini Live API.

---

## 3. User Interaction Flow

### 3.1 Default User Flow

1. User opens LLM Lens.
2. Latest AI news feed is displayed (filtered and prioritized).
3. User clicks on a headline.
4. Infographic is generated and displayed.
5. User gains a quick understanding of the key development in under 30 seconds.

### 3.2 Explain Mode (Optional)

1. User clicks "Explain" on an infographic.
2. Gemini Live API provides a spoken explanation:

   * What changed
   * Why it matters
   * Who benefits
3. Optional visual highlighting points to sections of the infographic.

### 3.3 Background Autonomous Flow (Marathon Agent)

1. Agent continuously monitors news sources.
2. Determines infographic-worthiness.
3. Extracts, verifies, and organizes key information.
4. Plans visual layout.
5. Generates infographic via Creative Autopilot.
6. Performs self-critique and regenerates if necessary.
7. Publishes the infographic to the feed autonomously.

---

## 4. Technical Stack

* **Gemini 3 Pro:** Reasoning, fact-checking, layout planning.
* **Gemini Live API:** Optional live explanation mode.
* **Nano Banana Pro:** Multimodal high-resolution infographic generation.
* **Web UI:** User interface for news feed and infographic interaction.
* **Marathon Agent:** Orchestrates continuous autonomous operation.

---

## 5. Summary

LLM Lens combines **continuous reasoning, fact verification, and high-quality visual generation** to provide users with a fast, accurate, and visually intuitive way to digest AI, LLM, and chip industry developments. The system operates autonomously while also allowing optional user interaction through Live explanations, making it both practical and demo-ready for a hackathon setting.
