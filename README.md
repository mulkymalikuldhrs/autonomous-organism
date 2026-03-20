# 🧬 ORGANISME SAAS OTONOM (GEN-4)

## Overview
This is an autonomous digital species designed to discover human problems, build SaaS solutions, and generate revenue without human intervention. Built on a consolidated Python Gen-4 architecture.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js & npm
- [Ollama](https://ollama.com/) (Optional, but recommended for local LLM)

### Setup
1. **Install Dependencies:**
   ```bash
   npm install
   pip install -r backend/requirements.txt
   playwright install chromium
   ```

2. **Environment Variables:**
   Create a `.env` file (optional):
   ```env
   HF_TOKEN=your_huggingface_token_for_fallback
   OLLAMA_URL=http://localhost:11434/api/generate
   ```

3. **Run the Organism:**
   You can run the full system (Backend + Frontend) using the verification script or manually:

   **Manual Startup:**
   - Backend: `python3 -m backend.main` (starts on port 8000)
   - Frontend: `npm run dev` (starts on port 8080)

4. **Verify System:**
   ```bash
   python3 -m backend.test_organism
   python3 verify_organism_ui.py
   ```

## 🧠 System Architecture (Gen-4)
- **Sense Engine:** Uses Playwright to scrape platforms like HackerNews, Reddit, and IndieHackers.
- **Decision Core:** Uses TF-IDF clustering and LLM analysis to score and select the best problems.
- **SaaS Factory:** Generates complete MVP boilerplate (FastAPI + React + Docker).
- **Growth Engine:** Automatically generates multi-stage marketing campaigns.
- **Evolution Engine:** Adjusts scoring weights dynamically based on revenue and traffic performance.
- **Immune System:** Monitors system health and protects resources.

## 📁 File Structure
- `backend/`: Core autonomous logic (FastAPI, SQLAlchemy, Engines).
- `src/`: React/Tailwind frontend dashboard.
- `products/`: Output directory for generated SaaS products.
- `growth_outbox/`: Generated marketing content.

---
*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*
