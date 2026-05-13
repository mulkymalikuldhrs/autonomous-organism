# 🧬 ORGANISME SAAS OTONOM GEN-4.1

Autonomous SaaS Organism that discovers problems, builds solutions, and generates revenue without human intervention.

## 🚀 Architecture (Gen-4.1)

- **Backend**: FastAPI (Python 3.12)
- **Frontend**: React + Vite + Tailwind + shadcn/ui
- **Database**: SQLite (Autonomous Memory)
- **Engines**:
  - `Sense`: Real-world scraping (Playwright)
  - `Decision`: LLM-based analysis (Ollama/Fallback)
  - `Factory`: Automated project scaffolding
  - `Growth`: Autonomous marketing & traffic
  - `Monetization`: Revenue tracking & simulation
  - `Immune System`: Safety throttling & health checks

## 🛠️ Getting Started

### Local Development

1. **Setup Backend**:
   ```bash
   pip install -r backend/requirements.txt
   python3 -m backend.main
   ```

2. **Setup Frontend**:
   ```bash
   npm install
   npm run dev -- --port 8080
   ```

3. **Run Organism Cycle**:
   ```bash
   python3 -m backend.engine.scheduler
   ```

### Docker Setup

```bash
docker-compose up --build
```

## 🧬 Blueprint

See [BLUEPRINT.md](BLUEPRINT.md) for the technical vision and mission.

---
*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*
