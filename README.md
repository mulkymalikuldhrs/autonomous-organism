# ORGANISME SAAS OTONOM (Gen-4)

Sistem otonom yang dirancang untuk mencari masalah, membangun solusi, dan berevolusi secara mandiri tanpa ketergantungan pada vendor mahal.

## Fitur Utama (Upgrade Gen-4)

- **Sense Engine (Indra)**: Menggunakan Playwright untuk scraping dinamis (Reddit, HackerNews, ProductHunt, IndieHackers). Dilengkapi dengan LLM Noise Filter.
- **Decision Core (Otak)**: Algoritma scoring tertimbang berdasarkan volume keluhan, emosi negatif, kemudahan otomasi, dan potensi pendapatan.
- **SaaS Factory (Rahim)**: Membuat struktur proyek lengkap (FastAPI, React, Docker) bukan sekadar boilerplate.
- **Growth Engine (Mulut)**: Kampanye pemasaran multi-tahap (Pre-Launch, Launch, Post-Launch).
- **Evolution Engine (Ingatan & Belajar)**: Menyesuaikan parameter scoring berdasarkan performa produk (pendapatan & traffic).
- **Immune System (Anti Gila)**: Monitoring kesehatan sistem (error rate, disk space, DB integrity) dengan fitur isolasi otomatis.

## Struktur Proyek

- `/frontend`: Dashboard monitoring berbasis React + Vite + Tailwind.
- `/backend`: Server FastAPI yang mengelola agen dan data.
- `/backend/engine`: Logika inti dari setiap indra dan organ organisme.
- `/products`: Direktori hasil produksi SaaS yang dibangun secara otomatis.

## Cara Menjalankan

### Backend
1. Install dependensi: `pip install -r backend/requirements.txt`
2. Install browser Playwright: `playwright install chromium`
3. Jalankan server: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`

### Frontend
1. Install dependensi: `npm install`
2. Jalankan development server: `npm run dev`

## Lisensi
Open Source - Gunakan untuk kebaikan spesies digital.
