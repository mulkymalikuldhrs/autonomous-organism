# ORGANISME SAAS OTONOM (Gen-4)

## Architecture Overview
This is a self-evolving autonomous organism designed to identify human problems, build solutions, and generate revenue without human intervention.

### 8-Stage Autonomous Lifecycle
1. **Sense (Indra)**: Scans Reddit, HackerNews, ProductHunt, and RSS feeds using Playwright and BeautifulSoup to collect raw user complaints.
2. **Decision (Otak)**: Uses TF-IDF, KMeans clustering, and LLM-deep analysis to score problems based on volume, negative emotion, automation ease, and revenue potential.
3. **Factory (Rahim)**: Generates full-stack SaaS MVPs (FastAPI + React + Docker) based on the top-scored idea.
4. **Spawner (Agent Lifecycle)**: Manages a team of autonomous sub-agents (Research, Builder, Growth, Support) with distinct personalities and lifecycles.
5. **Growth (Mulut)**: Generates multi-stage marketing campaigns (Pre-Launch, Launch, Post-Launch) for various social channels.
6. **Monetization (Perut)**: Simulates and tracks revenue models (Subscription, Affiliate, etc.) based on traffic and conversion metrics.
7. **Evolution (Self-Upgrade)**: Analyzes performance logs to dynamically adjust Decision Core weights and system strategies.
8. **Immune (Anti-Gila)**: Monitors system health, error rates, and resource usage (disk space) to prevent runaway processes.

## Operational Instructions

### Backend Setup
1. Install dependencies: `pip install -r backend/requirements.txt`
2. Run FastAPI: `python3 -m backend.main` (runs on port 8000)
3. Integration Tests: `python3 -m backend.test_organism`

### Frontend Setup
1. Install dependencies: `npm install`
2. Run Vite: `npm run dev` (runs on port 8080, proxies `/api` to 8000)

### Verification
Visual verification can be performed using the `verify_organism_ui.py` script which captures dashboard screenshots.

## Rules of Life
- **Autonomous**: No manual operation required for daily cycles.
- **Self-Terminating**: The organism can stop or "suicide" if it detects harm to the owner's moral or financial well-being.
- **Evolutionary**: Successes are reinforced; failures are logged and used to tune future iterations.

"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."
