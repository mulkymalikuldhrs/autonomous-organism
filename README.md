# ORGANISME SAAS OTONOM (Gen-4)

Sistem otonom yang dirancang untuk mencari masalah, membangun solusi, dan berevolusi secara mandiri tanpa ketergantungan pada vendor mahal.

*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*

---

## 🧬 Arsitektur Organisme

Organisme ini bekerja dalam siklus 8-tahap yang dijalankan secara otomatis oleh `Scheduler`:

1.  **Sense Engine (Indra)**: Mengumpulkan data dari Reddit, HackerNews, dll. menggunakan Playwright.
2.  **Decision Core (Otak)**: Menganalisis masalah menggunakan TF-IDF/KMeans dan LLM untuk menentukan ide SaaS terbaik.
3.  **SaaS Factory (Rahim)**: Membangun produk MVP lengkap (Backend FastAPI, Frontend React).
4.  **Agent Spawner**: Mengelola armada sub-agent (Builder, Growth, Support) untuk tugas spesifik.
5.  **Growth Engine (Mulut)**: Membuat konten pemasaran otomatis untuk berbagai channel.
6.  **Monetization Engine (Perut)**: Menjalankan model bisnis dan melacak pendapatan (Affiliate, SaaS, dll).
7.  **Evolution Engine**: Mengatur ulang bobot keputusan berdasarkan data pendapatan dan trafik nyata.
8.  **Immune System**: Memastikan sistem tetap sehat dan mencegah perilaku "runaway" atau berbahaya.

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, FastAPI, SQLAlchemy (SQLite), Playwright, Scikit-learn, NLTK.
- **Frontend**: Vite, React, TypeScript, Tailwind CSS, Shadcn/UI.
- **LLM**: Ollama (Lokal - Llama3/Mistral) atau HuggingFace Inference API (Backup).

## 🚀 Cara Menjalankan

### 1. Persiapan Lingkungan
Clone repositori dan masuk ke direktori proyek.

### 2. Backend (Jantung & Otak)
```bash
# Install dependensi
pip install -r backend/requirements.txt

# Install browser untuk Sense Engine
python3 -m playwright install chromium

# Jalankan server API dan Scheduler
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 3. Frontend (Dashboard Monitoring)
```bash
# Install dependensi
npm install

# Jalankan dashboard
npm run dev
```
Dashboard dapat diakses di `http://localhost:8080`.

## ⚙️ Konfigurasi (.env)
Buat file `.env` di root untuk menggunakan LLM eksternal:
```env
HF_TOKEN=your_huggingface_token_here (Opsional, untuk backup cloud)
OLLAMA_URL=http://localhost:11434/api/generate (Default untuk Ollama lokal)
```

## 📂 Struktur Direktori
- `backend/`: Kode sumber Python.
- `backend/engine/`: Logika organ organisme.
- `src/`: Dashboard monitoring (React).
- `products/`: SaaS yang berhasil dibangun oleh Factory.
- `growth_outbox/`: Konten pemasaran yang dihasilkan.

---
**Status**: OTONOM & AKTIF (Gen-4)
**Misi**: Evolusi brutal menuju profitabilitas.
