# 🤖 AGENTS.md - ORGANISME SAAS OTONOM

## Overview
This organism is a self-evolving species designed to discover, build, and monetize SaaS products autonomously.

## 📂 Architecture (Gen-4)
- **Sense Engine**: Scrapes HackerNews, Reddit, and ProductHunt using Playwright.
- **Decision Core**: Analyzes problems using clustering (TF-IDF/KMeans) and LLM-based scoring.
- **SaaS Factory**: Generates Dockerized FastAPI/React solutions.
- **Agent Spawner**: Manages specialized sub-agents with distinct personalities.
- **Growth Engine**: Generates multi-stage marketing campaigns.
- **Monetization Engine**: Tracks revenue and simulates conversion based on traffic.
- **Evolution Engine**: Adjusts system weights based on product performance.
- **Immune System**: Monitors health (Disk, Errors, DB) and prevents runaway processes.

## 🚀 Operational Instructions

### 1. Environment Setup
```bash
# Backend
pip install -r backend/requirements.txt
python3 -m playwright install chromium

# Frontend
npm install
```

### 2. Running the System
```bash
# Start Backend
python3 -m backend.main &

# Start Frontend
npm run dev
```

### 3. Verification
- **Integration Test**: `python3 -m backend.test_organism`
- **Visual Verification**: `python3 verify_organism_ui.py` (Captures screenshots to `/home/jules/verification/`)

## 🧬 Life Loop
The system runs in an infinite loop (`backend/engine/scheduler.py`), executing all 8 stages hourly. Manual overrides are available on the dashboard at port 8080.

## ⚠️ Safety Constraints
- **Suicide Rule**: System will terminate if it detects harm to owner.
- **Immune Thresholds**: Max 10 errors/hr or 5 products/hr.
- **Zero Cost**: Only utilizes free cloud tiers and local resources.

---
"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."
