# 🧬 AGENT OPERATIONAL INSTRUCTIONS

## Overview
This repository contains the **ORGANISME SAAS OTONOM (Gen-4)**. It is a self-evolving digital species designed to identify human problems, build solutions (SaaS), and manage its own growth and monetization autonomously.

## Architecture (Gen-4)
The organism operates through an 8-stage lifecycle orchestrated by the `backend/engine/scheduler.py`:

1.  **SENSE**: Scrapes problems from Reddit, HackerNews, ProductHunt, etc., using Playwright and BeautifulSoup.
2.  **DECISION**: Uses TF-IDF vectorization, KMeans clustering, and LLM analysis to prioritize the most viable problems.
3.  **FACTORY**: Generates product blueprints and basic file structures for new Micro-SaaS solutions.
4.  **SPAWNER**: (Future) Spawns specialized sub-agents to handle specific product tasks.
5.  **GROWTH**: Generates marketing content and simulates user acquisition.
6.  **MONETIZATION**: Calculates revenue potential and logs simulated/actual income.
7.  **EVOLUTION**: Adjusts its own internal weights and strategies based on performance logs.
8.  **IMMUNE**: Monitors system health, resource usage, and error rates to prevent "instability."

## Technical Stack
-   **Backend**: FastAPI (Python 3.12+)
-   **Database**: SQLite (SQLAlchemy)
-   **Frontend**: React + Vite + Tailwind CSS + shadcn/ui
-   **LLM**: Ollama (Local) with HuggingFace (Cloud) fallback
-   **Scraping**: Playwright (Headless Chromium)

## Operational Commands
-   **Install Dependencies**: `pip install -r backend/requirements.txt && npm install`
-   **Run Backend**: `uvicorn backend.main:app --reload --port 8000`
-   **Run Frontend**: `npm run dev` (Vite will proxy `/api` to port 8000)
-   **Run Integration Test**: `python3 -m backend.test_organism`
-   **Visual Verification**: Use `verify_organism_ui.py` to capture dashboard state.

## Safety Protocols (IMMUNE SYSTEM)
-   The organism must strictly avoid any actions that harm the owner morally, socially, or financially.
-   It is capable of automatic self-termination (suicide) if critical error thresholds are met or disk space is low.
-   The "Self-Evolution" rule mandates that it must upgrade its own models and strategies without human intervention.
