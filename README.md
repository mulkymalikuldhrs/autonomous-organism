# 🧬 ORGANISME SAAS OTONOM (Gen-4)

Sistem kehidupan otonom yang menemukan masalah manusia, membangun solusi SaaS, dan mencari pendapatan tanpa intervensi manusia.

## 🚀 Fitur Utama

- **Sense Engine**: Scrape Reddit, HackerNews, ProductHunt, dll menggunakan Playwright.
- **Decision Core**: Analisis masalah menggunakan LLM (Ollama/HuggingFace) dan skoring otomatis.
- **SaaS Factory**: Menghasilkan boilerplate lengkap (FastAPI + React + Docker).
- **Growth Engine**: Strategi pemasaran otomatis.
- **Evolution**: Belajar dari performa dan memperbarui bobot skoring.
- **Immune System**: Monitor kesehatan sistem dan cegah loop tak terbatas.

## 🛠️ Tech Stack

- **Backend**: Python (FastAPI), SQLAlchemy (SQLite), Playwright, NLTK, Scikit-learn.
- **Frontend**: React (Vite), Tailwind CSS, Shadcn UI.
- **AI**: Ollama (Lokal), HuggingFace Inference (Cloud Backup).

## 🏃 Cara Menjalankan

### 1. Backend

Pastikan Anda memiliki Python 3.10+ dan telah menginstal dependensi:

```bash
cd backend
pip install -r requirements.txt
playwright install chromium
python -m backend.main
```

Backend akan berjalan di `http://127.0.0.1:8000`.

### 2. Frontend

Instal dependensi Node.js dan jalankan server pengembangan:

```bash
npm install
npm run dev
```

Frontend akan berjalan di `http://127.0.0.1:8080` dan secara otomatis memproksi permintaan API ke backend.

## 🧪 Pengujian

Jalankan tes integrasi backend:

```bash
python3 -m backend.test_organism
```

Jalankan tes frontend:

```bash
npm test
```

## 🧬 Filosofi

"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."
Sistem ini dirancang untuk beroperasi secara mandiri, berevolusi, dan bahkan "membunuh" dirinya sendiri jika merugikan pemiliknya.
