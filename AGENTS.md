# Autonomous Organism - Operational Instructions

This repository contains the Gen-4 implementation of the Autonomous SaaS Organism, a self-evolving system designed to identify problems, build solutions, and generate revenue.

## 🧬 Architecture Overview

The system follows an 8-stage lifecycle orchestrated by the `backend/engine/scheduler.py`:
1. **Sense**: Scrapes platforms like Hacker News, Reddit, and IndieHackers for user complaints.
2. **Decision**: Clusters problems and scores them based on volume, negative sentiment, and automation potential.
3. **Factory**: Generates a full SaaS project structure (FastAPI + React + Docker) for selected ideas.
4. **Growth**: Creates multi-stage marketing campaigns for generated products.
5. **Monetization**: Simulates and tracks revenue from active products.
6. **Evolution**: Tunes system weights and strategies based on performance logs.
7. **Immune**: Monitors system health, error rates, and resource usage.
8. **Spawner**: Manages specialized sub-agents with distinct personality traits.

## 🚀 Running the System

### Prerequisites
- Python 3.10+
- Node.js & npm
- [Optional] Ollama running locally for local LLM inference

### Setup
1. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   python3 -m playwright install chromium
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```

### Local Execution
1. Start the backend:
   ```bash
   python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```
2. Start the frontend:
   ```bash
   npm run dev
   ```
3. Access the dashboard at `http://localhost:8080`.

## 🧪 Testing & Verification

- **Backend Integration Test**:
  ```bash
  python3 -m backend.test_organism
  ```
- **UI Verification**:
  ```bash
  python3 verify_organism_ui.py
  ```

## ⚠️ Safety Protocols (Immune System)
- The system will automatically throttle or pause if error rates exceed 10/hr.
- Automatic log cleanup is triggered if disk space falls below 1GB.
- The system includes a 'suicide' protocol to protect the owner from reputational or financial harm if specified thresholds are crossed.

---
*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*
