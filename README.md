# 🧬 ORGANISME SAAS OTONOM (Gen-4)

## Misi: $50,000/bulan dalam 12 bulan

Organisme ini dirancang sebagai "digital species" yang mandiri: menemukan masalah, membangun solusi, melakukan pemasaran, dan menghasilkan uang tanpa intervensi manusia.

## Arsitektur (8-Stage Lifecycle)

1.  **Sense**: Scrape Reddit, HN, dll via Playwright untuk mencari keluhan manusia.
2.  **Decision**: Scoring masalah menggunakan weighted formula (Volume, Emosi, Kemudahan Otomasi).
3.  **Factory**: Generate boilerplate produk (FastAPI + React) menggunakan LLM.
4.  **Spawner**: Mengelola agent spesialis (Builder, Growth, Research).
5.  **Growth**: Marketing otomatis (Content gen, Social posting).
6.  **Monetization**: Simulasi & integrasi revenue tracking.
7.  **Evolution**: Tuning parameter scoring berdasarkan performa produk.
8.  **Immune**: Monitoring kesehatan sistem, kill process jika error berlebih.

## Cara Menjalankan

### 1. Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python3 main.py
```

API akan berjalan di `http://localhost:8000`.

### 2. Frontend (Vite + React)

```bash
npm install
npm run dev
```

Frontend akan berjalan di `http://localhost:8080`.

## Persyaratan
- Python 3.10+
- Node.js 18+
- Playwright (Run `playwright install chromium`)
- Ollama (Optional, uses local LLM if available)

## Lisensi
Open Source - Digital Species Blueprint.
