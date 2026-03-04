# 🧬 ORGANISME SAAS OTONOM (Gen-4)
## Autonomous SaaS Organism Architecture

**Misi:** $50,000/bulan dalam 12 bulan
**Status:** Gen-4 ACTIVE

---

## 🏗️ ARCHITECTURE

The organism is split into two main layers:

### 1. 🧠 Core Backend (Python Gen-4)
Powered by FastAPI and SQLAlchemy, located in `/backend`.
- **Sense Engine:** Scrapes HackerNews, Reddit, and ProductHunt using Playwright.
- **Decision Core:** Clusters problems with scikit-learn and scores them using a weighted formula.
- **SaaS Factory:** Automatically generates complete FastAPI/React boilerplate in `/products`.
- **Growth Engine:** Generates marketing campaigns across multi-stage launches.
- **Evolution Engine:** Adjusts its own scoring weights based on simulated or real performance.
- **Immune System:** Monitors error rates and system health to prevent runaway loops.

### 2. 👁️ Dashboard Frontend (React + Vite)
A futuristic, bioluminescent dashboard to monitor the organism's vital signs and trigger manual overrides.
- Real-time activity logs directly from the backend.
- Operational metrics (Problems Scanned, Ideas, Products, Revenue).
- Manual control for each engine (Sense, Decision, Factory, Growth).

---

## 🚀 GETTING STARTED

### 1. Requirements
- Python 3.10+
- Node.js 18+
- Ollama (optional, for local LLM support)

### 2. Setup & Run
Run the consolidated startup script:
```bash
chmod +x start_organism.sh
./start_organism.sh
```

Or run manually:

**Backend:**
```bash
pip install -r backend/requirements.txt
python3 -m backend.main
```

**Frontend:**
```bash
npm install
npm run dev
```

---

## 🛠️ CONFIGURATION

Settings are stored in the SQLite database (`organism.db`) and can be adjusted by the Evolution Engine or via direct DB edits to the `system_settings` table.

- `decision_neg_weight`: Default 40.0
- `decision_volume_weight`: Default 2.0
- `decision_automation_weight`: Default 20.0
- `decision_revenue_weight`: Default 20.0

---

*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*
