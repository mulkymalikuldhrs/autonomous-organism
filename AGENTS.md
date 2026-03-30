# ORGANISME SAAS OTONOM (Gen-4) - Agent Operational Guidelines

## Overview
This organism is a self-evolving digital species designed to identify human problems, build SaaS solutions, and generate revenue autonomously. It operates on an 8-stage lifecycle.

## 8-Stage Autonomous Lifecycle
1.  **Sense**: Scans digital sources (HN, Reddit, etc.) for user complaints using Playwright.
2.  **Decision**: Clusters problems and scores them using a weighted formula (Sentiment, Volume, Automation Ease, Revenue Potential).
3.  **Factory**: Generates complete technical specifications and boilerplate (FastAPI + React + Docker) for selected ideas.
4.  **Spawner**: Spawns specialized autonomous sub-agents (Research, Builder, Growth, Support) with distinct personality traits.
5.  **Growth**: Generates multi-stage marketing campaigns (Pre-Launch, Launch, Post-Launch) for products.
6.  **Monetization**: Simulates and tracks revenue based on traffic conversion logs.
7.  **Evolution**: Adjusts system weights and strategies based on performance metrics (Revenue, Clicks).
8.  **Immune**: Monitors system health (errors, disk space, runaway processes) and performs self-correction.

## Technical Architecture
- **Backend**: FastAPI (Python 3.12+)
- **Database**: SQLite (SQLAlchemy models)
- **Frontend**: React + Vite + Tailwind CSS (Proxied to backend)
- **LLM**: Ollama (Local) with multi-stage fallback to HF and structured templates.

## Operational Commands
- Run backend: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
- Run frontend: `npm run dev` (port 8080)
- Integration test: `python3 -m backend.test_organism`
- UI Verification: `python3 verify_organism_ui.py`

## Verification Artifacts
- **Dashboard**: `http://localhost:8080`
- **Logs**: `/api/logs`
- **Metrics**: `/api/metrics`
- **Verification Media**: `/home/jules/verification/screenshots/dashboard_verification.png`

---
*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*
