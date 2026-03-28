# 🤖 AGENT OPERATIONAL INSTRUCTIONS

## 🧬 Gen-4 Autonomous Organism Overview
This organism is a self-evolving species designed to identify human problems, architect SaaS solutions, and manage their lifecycle autonomously. It operates on an 8-stage lifecycle orchestrated by a central scheduler.

### 8-Stage Lifecycle
1. **Sense**: Scrapes sources (Reddit, HackerNews, IndieHackers) using Playwright and BeautifulSoup to find raw complaints.
2. **Decision**: Clusters problems using TF-IDF/KMeans and performs deep LLM analysis to score ideas by revenue potential and automation ease.
3. **Factory**: Generates a full-stack structure (FastAPI + React/Tailwind) for the top-scoring idea.
4. **Spawner**: Manages autonomous sub-agents (Research, Builder, Growth, Support) with unique personality traits.
5. **Growth**: Executes multi-stage marketing campaigns and simulates user traffic.
6. **Monetization**: Simulates and logs revenue based on product performance.
7. **Evolution**: Dynamically tunes system weights (e.g., pain sensitivity) based on financial and traffic performance.
8. **Immune**: Monitors system health and resource usage to prevent runaway processes.

## 🛠 Operational Commands

### Environment Setup
```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node dependencies
npm install

# Setup Playwright
python3 -m playwright install chromium
```

### Running the Organism
```bash
# Start the full autonomous loop (FastAPI + Scheduler)
python3 -m backend.main

# Start the Frontend Dashboard
npm run dev
```

### Verification & Testing
```bash
# Run full lifecycle integration test
python3 -m backend.test_organism

# Visual dashboard verification
python3 verify_organism_ui.py
```

## 📂 File Structure (Gen-4)
- `backend/main.py`: Entry point for the FastAPI API and lifecycle scheduler.
- `backend/models.py`: Database schema for problems, ideas, products, agents, and logs.
- `backend/engine/`: Core logic for each lifecycle stage.
- `products/`: Generated SaaS product artifacts.
- `src/`: React frontend for the autonomous monitoring dashboard.

## ⚠️ Safety Protocols (Immune System)
- Max iterations per task are enforced to prevent LLM loops.
- Error thresholds automatically trigger agent termination if failures exceed limits.
- The organism can be stopped at any time by terminating the main process.
- Automatic self-termination is implemented for critical resource protection.
