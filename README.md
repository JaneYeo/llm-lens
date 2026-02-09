# LLM Lens: Strategic AI Intelligence & Analysis Platform

[![Autonomous Pipeline](https://github.com/JaneYeo/llm-lens/actions/workflows/brain.yml/badge.svg)](https://github.com/JaneYeo/llm-lens/actions/workflows/brain.yml)
[![Deployment](https://img.shields.io/badge/Status-Deployed%20on%20Vercel-success)](https://llm-lens.vercel.app)

LLM Lens is an enterprise-grade autonomous intelligence platform designed to aggregate, verify, and synthesize global developments in Artificial Intelligence. The system transforms high-volume technical data and industry signals into structured, high-signal analytical insights and professional infographics.

---

## 🏛️ System Architecture

The platform utilizes a multi-agent, serverless architecture to ensure high availability and efficiency at scale.

| Component | Provider / Technology | Strategic Role |
| :--- | :--- | :--- |
| **Intelligence Layer** | Google Gemini (Pro/Flash) | Automated synthesis, fact extraction, and visual generation. |
| **Data Infrastructure**| Turso (LibSQL) | Distributed edge database for optimized global synchronization. |
| **Asset Orchestration**| Cloudinary | Automated media optimization and CDN delivery. |
| **Automation Engine** | GitHub Actions | Scheduled serverless execution of the autonomous brain cycle. |
| **Web Framework** | Next.js | High-performance reactive interface for data consumption. |

---

## 📡 Intelligence Sources

The platform aggregates high-signal data from premium technical and academic sources:

*   **Academic Research**: Direct integration with the **ArXiv API** (cs.AI) for cutting-edge machine learning papers.
*   **Industry Reporting (RSS)**: Real-time feeds from established tech press including **TechCrunch**, **VentureBeat**, **Wired**, **The Verge**, **MIT Tech Review**, and **The Guardian**.
*   **Developer Signals**: Narrative and community sentiment from curated subreddits (r/MachineLearning, r/LocalLLaMA, r/OpenAI).

---

## 🎯 Strategic Value

*   **For AI Researchers**: Automated Technical synthesis of ArXiv research papers into structured fact-sheets.
*   **For Strategic Analysts**: Real-time tracking of AI industry shifts with a focus on signal over noise.
*   **For Tech Executives**: High-level visual mapping of the AI landscape for accelerated decision-making.

---

## 🧩 Open Source & Ecosystem Participation

This project integrates and contributes to the following open-source ecosystems and platform providers:

*   **Next.js (Vercel)**: The foundational React framework for production-grade web applications.
*   **LibSQL (Turso)**: The open-source evolution of SQLite, enabling decentralized data management.
*   **GitHub Actions**: Providing the distributed infrastructure for autonomous workload execution.
*   **Google Gemini**: Large Language Model infrastructure for advanced semantic processing.
*   **Cloudinary**: Intelligent media management and global content distribution.
*   **React & Framer Motion**: Core technologies for building responsive, high-performance user interfaces.

---

## 🚀 Technical Implementation

### Autonomous Pipeline Cycle
The system operates on an autonomous "Marathon Loop" consisting of four distinct phases:
1.  **Ingestion**: Aggregation of research (ArXiv), developer signals (Reddit), and industry reports.
2.  **Synthesis**: Semantic analysis and fact verification using generative intelligence.
3.  **Visualization**: Generation of bespoke analytical infographics for high-impact stories.
4.  **Synchronization**: Real-time metadata and asset propagation to cloud-native infrastructure.

### Local Development Environment
```bash
# Initialize Front-end
cd web
npm i
npm run dev

# Execute Intelligence Cycle
python execution/marathon_loop.py --run-once
```

---

## ⚖️ License
Licensed under the MIT License. Developed as a high-performance demonstration of autonomous agentic workflows.
