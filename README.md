# ORGANISME SAAS OTONOM

## Overview
Proyek ini adalah implementasi dari **Autonomous SaaS Organism**. Sistem ini dirancang untuk menemukan masalah manusia secara mandiri, membangun solusi (blueprint), dan melakukan promosi tanpa intervensi manusia.

## Arsitektur
- **Frontend**: Vite + React + Tailwind + Shadcn/UI. Menampilkan dashboard kesehatan organisme.
- **Backend**: Python FastAPI. Menjalankan mesin inti organisme.
- **Engines**:
  - **Sense**: Melakukan scraping real-time dari Hacker News (dan sumber lain) untuk mencari keluhan/masalah.
  - **Decision**: Menganalisis masalah menggunakan TF-IDF, KMeans Clustering, dan Sentiment Analysis untuk memilih ide MVP terbaik.
  - **Factory**: Menghasilkan blueprint produk di direktori `products/`.
  - **Growth**: Menghasilkan konten promosi di direktori `growth_outbox/`.
  - **Immune**: Memantau kesehatan sistem dan mendeteksi anomali.
  - **Scheduler**: Mengelola siklus hidup organisme secara otonom.

## Cara Menjalankan

### 1. Persiapan Lingkungan
```bash
# Frontend
npm install

# Backend
pip install -r backend/requirements.txt
```

### 2. Menjalankan Organisme
Jalankan backend di terminal pertama:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Jalankan frontend di terminal kedua:
```bash
npm run dev
```

Organisme akan mulai bekerja secara otomatis setiap jam. Anda juga bisa memicu Sense atau Decision secara manual dari dashboard.

## Teknologi
- Python (FastAPI, SQLAlchemy, Scikit-learn, NLTK, BeautifulSoup)
- Node.js (React, Vite, TanStack Query)
- SQLite (Penyimpanan lokal)
- Ollama (Opsional, untuk LLM lokal)
