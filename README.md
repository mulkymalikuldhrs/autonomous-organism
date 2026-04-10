# ORGANISME SAAS OTONOM (Gen-4)

Blueprint Teknis – Gratis, Open Source, Otonom.

## Overview
This is a "Digital Species" designed to independently identify human problems, engineer solutions, and evolve its own strategies for growth and monetization.

### 8-Stage Autonomous Lifecycle
1.  **👁️ SENSE**: Scans global (HackerNews, Reddit) and Indonesian (Kaskus, Quora ID, YouTube ID) sources using Playwright.
2.  **🧠 DECISION**: Clusters problems using Scikit-Learn (TF-IDF + KMeans) and scores them based on sentiment and ROI potential.
3.  **🏭 FACTORY**: Generates full-stack code (FastAPI + React) with a bioluminescent design system.
4.  **🧬 SPAWNER**: Manages autonomous sub-agents (Builder, Growth, Research, Support).
5.  **📢 GROWTH**: Creates multi-stage marketing campaigns across Twitter, Reddit, and Telegram.
6.  **💰 MONETIZATION**: Simulates and tracks revenue from built products.
7.  **🔄 EVOLUTION**: Adjusts internal scoring weights based on traffic and revenue performance.
8.  **🛡️ IMMUNE**: Monitors system vitals and ensures the "Suicide Clause" is respected if the organism becomes harmful.

## Technical Stack
- **Backend**: FastAPI (Python 3.12+)
- **Frontend**: React + Vite + Tailwind CSS
- **Database**: SQLite (SQLAlchemy)
- **Intelligence**: Ollama (Local LLM) / HuggingFace (Cloud Backup)
- **Automation**: Playwright, BeautifulSoup4, NLTK

## Getting Started

### Local Development
1. **Install Python Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. **Install Node Dependencies**:
   ```bash
   npm install
   ```
3. **Run the Organism**:
   ```bash
   # Terminal 1: Backend
   python3 -m backend.main

   # Terminal 2: Frontend
   npm run dev
   ```
4. **Access Dashboard**: `http://localhost:8080`

## Verification
Run the integrated test suite:
```bash
python3 -m backend.test_organism
```

Run visual E2E verification:
```bash
python3 verify_organism_ui.py
```

---
*Status: PRODUCTION-READY GEN-4*
