# 🧬 ORGANISME SAAS OTONOM (Gen-4)

## Project info
**Misi**: Mencapai revenue $50,000/bulan dalam 12 bulan.
**Visi**: "Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."

## Tech Stack (Gen-4 Architecture)
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React + Tailwind CSS + Vite
- **Database**: SQLite (Local) / Supabase (Optional)
- **LLM**: Ollama (Local) / HuggingFace (Cloud Free)
- **Automation**: Playwright, BeautifulSoup, NLTK, Scikit-learn

## How to Run

### 1. Backend Setup
```sh
cd backend
pip install -r requirements.txt
python -m playwright install chromium
python main.py
```
Backend runs on `http://127.0.0.1:8000`.

### 2. Frontend Setup
```sh
npm install
npm run dev
```
Frontend runs on `http://127.0.0.1:8080`.

## Autonomous Lifecycle (8-Stage Loop)
1. **SENSE**: Scrapes Reddit, HN, IndieHackers for human problems.
2. **DECISION**: Scores ideas using weighted formulas and LLM analysis.
3. **FACTORY**: Generates full SaaS project structures (Backend/Frontend/Docker).
4. **SPAWNER**: Manages specialized sub-agents (Research, Builder, Growth, Support).
5. **GROWTH**: Generates marketing campaigns across Twitter/Reddit/IH.
6. **MONETIZATION**: Simulates and tracks real revenue conversions.
7. **EVOLUTION**: Self-tunes scoring weights based on performance.
8. **IMMUNE**: Monitors system health and prevents runaway processes.

## Verification
- Run backend tests: `python3 -m backend.test_organism`
- Run visual E2E: `python3 verify_organism_ui.py`
