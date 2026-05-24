# 🧬 ORGANISME SAAS OTONOM (GEN-4.1)

Sistem otonom yang membiakkan bisnis, membunuh yang lemah, dan berevolusi sendiri tanpa API berbayar.

## 🚀 Fitur Utama (Gen-4.1)

- **Autonomous Lifecycle**: 8 tahap siklus hidup (Sense, Decision, Factory, Spawner, Growth, Monetization, Evolution, Immune).
- **Indra Playwright**: Scraping dinamis sumber masalah manusia (Reddit, HN, ProductHunt).
- **Decision Core NLTK**: Analisis sentimen dan scoring strategis untuk memilih ide terbaik.
- **SaaS Factory**: Pembuatan otomatis boilerplate SaaS (FastAPI + React + Docker).
- **Self-Evolution**: Penyesuaian bobot scoring secara otomatis berdasarkan data performa.
- **Immune System**: Monitoring kesehatan sistem dan proteksi terhadap kegagalan runaway.

## 🛠️ Stack Teknologi

- **Backend**: Python 3.12, FastAPI, SQLAlchemy, SQLite.
- **Frontend**: React (Vite), Tailwind CSS, Shadcn UI.
- **Intelligence**: Ollama (Local LLM), NLTK, Scikit-learn.
- **Automation**: Playwright, BeautifulSoup4.

## 🏁 Quick Start

### 1. Prasyarat
- Python 3.12+
- Node.js & npm
- Ollama (opsional, sistem akan menggunakan fallback jika tidak ada)

### 2. Instalasi
```bash
# Install Python dependencies
pip install -r backend/requirements.txt
playwright install --with-deps chromium

# Install Frontend dependencies
npm install
```

### 3. Menjalankan Sistem
```bash
# Terminal 1: Backend
python3 -m backend.main

# Terminal 2: Frontend
npm run dev -- --port 8080
```

### 4. Verifikasi
```bash
python3 verify_organism_ui.py
```

## 📐 Blueprint
Lihat [BLUEPRINT.md](BLUEPRINT.md) untuk detail arsitektur dan filosofi desain.

---
*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*
