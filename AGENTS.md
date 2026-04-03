# Operational Instructions for the Autonomous SaaS Organism (Gen-4)

## Overview
The Autonomous SaaS Organism is a self-evolving digital species designed to identify human problems, build solutions, and generate revenue without human intervention. This Gen-4 implementation is fully consolidated into a Python backend with a React frontend dashboard.

## Core Architecture (The 8-Stage Lifecycle)
The organism operates on a continuous loop managed by the `Scheduler` (`backend/engine/scheduler.py`).

1.  **Sense Engine** (`backend/engine/sense.py`):
    - Scrapes sources like HackerNews, Reddit, and ProductHunt using Playwright and RSS.
    - Filters noise using LLM to identify real user complaints.
2.  **Decision Core** (`backend/engine/decision.py`):
    - Clusters and scores problems based on a weighted formula (complaints, sentiment, automation ease, revenue potential).
    - Selects the top idea for implementation.
3.  **SaaS Factory** (`backend/engine/factory.py`):
    - Generates full-stack code (FastAPI + React + Docker) for the selected idea using LLM.
    - Persists products to the `products/` directory.
4.  **Agent Spawner** (`backend/engine/spawner.py`):
    - Deploys specialized agents (Research, Builder, Growth, Support) to manage products.
5.  **Growth Engine** (`backend/engine/growth.py`):
    - Generates marketing content for various channels (Twitter, Reddit, IndieHackers).
    - Outputs content to `growth_outbox/`.
6.  **Monetization Engine** (`backend/engine/monetization.py`):
    - Simulates and tracks revenue from active products.
7.  **Evolution Engine** (`backend/engine/evolution.py`):
    - Adjusts system weights based on performance logs to optimize future cycles.
8.  **Immune System** (`backend/engine/immune.py`):
    - Monitors system health, disk space, and error rates.
    - Can trigger self-termination if safety thresholds are exceeded.

## Operational Commands

### Environment Setup
1.  Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    npm install
    python3 -m playwright install chromium
    ```
2.  Set environment variables in `.env`:
    - `OLLAMA_URL` (optional, for local LLM)
    - `HF_TOKEN` (optional, for cloud fallback)

### Running the Organism
- **Backend**: `python3 -m backend.main` (Runs on port 8000)
- **Frontend**: `npm run dev` (Runs on port 8080 by default, proxied to 8000)

### Testing and Verification
- **Integration Test**: `python3 -m backend.test_organism`
- **UI Verification**: `python3 verify_organism_ui.py` (captured screenshot `dashboard_verification.png`)

## Maintenance and Logs
- **Database**: Local SQLite database `organism.db`.
- **Logs**: Real-time logs are visible on the dashboard and stored in the database.
- **Artifacts**:
    - `products/`: Generated SaaS product source code.
    - `growth_outbox/`: Generated marketing materials.

## Principles of Operation
- **Autonomy**: The organism is designed to run without human intervention.
- **Safety**: The 'Immune System' and 'Rules of Life' (in `BLUEPRINT.md`) ensure the organism does not harm its owner or become stagnant.
- **Evolution**: The system learns from every cycle. Pola gagal (failure patterns) are recorded and avoided in future iterations.
