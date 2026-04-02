# 🤖 AGENTS.md - ORGANISME SAAS OTONOM (GEN-4)

## 🧬 Operational Overview
This organism is a "digital species" designed to autonomously discover problems, build solutions, and generate revenue. It operates on an 8-stage lifecycle.

### 🔄 The 8-Stage Lifecycle
1.  **Sense**: Scans the digital world (Reddit, HN, IndieHackers) for human pain points using Playwright and RSS.
2.  **Decision**: Analyzes findings using a weighted formula (Volume, Sentiment, Automation Ease) and LLM deep analysis to choose the best MVP candidate.
3.  **Factory**: Automatically generates technical specs, backend (FastAPI), frontend (React), and Docker configurations for the chosen idea.
4.  **Spawner**: Maintains a healthy population of autonomous sub-agents (Research, Builder, Growth, Support) with varying personalities.
5.  **Growth**: Generates multi-stage marketing campaigns across multiple social channels.
6.  **Monetization**: Simulates and tracks revenue based on traffic logs and conversion rates.
7.  **Evolution**: Dynamically adjusts its own decision weights and strategies based on performance metrics (Revenue, CTR).
8.  **Immune System**: Monitors system vitals (Error rates, Disk space, Runaway processes) to ensure stability.

## 🛠 Tech Stack
- **Backend**: FastAPI (Python 3.12+)
- **Frontend**: React + Vite + Tailwind CSS (Bioluminescent Theme)
- **Database**: SQLite (SQLAlchemy)
- **AI**: Ollama (Local) with HuggingFace fallback.
- **Scraping**: Playwright + BeautifulSoup4.

## 🚀 Commands
- **Install Backend**: `pip install -r backend/requirements.txt`
- **Install Frontend**: `npm install`
- **Run System**: `python3 -m backend.main` (Starts backend + scheduler) & `npm run dev` (Starts frontend)
- **Verification**: `python3 verify_organism_ui.py` (Runs E2E verification)
- **Integration Test**: `python3 -m backend.test_organism`

## ⚖️ Core Directives
- **Zero Cost**: Only use free tiers and local resources.
- **Self-Termination**: Must be able to "kill" itself if it harms the owner's moral or financial well-being.
- **Evolution**: Prioritize learning from failures over human intervention.

---
*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*
