# 🧬 ORGANISME SAAS OTONOM (Gen-4)

Sistem otonom yang dirancang untuk menemukan masalah manusia, membangun solusi SaaS, dan berkembang secara mandiri.

## 🚀 Fitur Utama (Gen-4)

- **Sense Engine**: Menggunakan Playwright untuk scraping dinamis (HackerNews, Reddit, IndieHackers, ProductHunt).
- **Decision Core**: Analisis sentimen dan clustering masalah menggunakan scikit-learn & NLTK.
- **SaaS Factory**: Menghasilkan struktur produk lengkap (FastAPI + React/Tailwind + Docker).
- **Growth Engine**: Strategi pemasaran multi-channel otomatis.
- **Evolution Engine**: Penyesuaian bobot scoring berdasarkan performa produk di dunia nyata.
- **Immune System**: Monitoring kesehatan sistem dan terminasi proses berbahaya.

## 🛠️ Struktur Proyek

```text
.
├── backend/                # FastAPI Gen-4 Engine
│   ├── engine/             # Modul logika otonom
│   ├── main.py             # Entry point API & Scheduler
│   ├── models.py           # Skema database SQLite (SQLAlchemy)
│   └── test_organism.py    # Integrasi test lifecycle
├── src/                    # React Frontend (Dashboard Telemetri)
│   ├── hooks/              # Hook komunikasi backend
│   └── pages/              # Dashboard interaktif
├── products/               # Output SaaS yang dihasilkan (Auto-generated)
└── organism.db             # Database SQLite pusat
```

## ⚙️ Cara Menjalankan

### 1. Backend (Python)
Pastikan Python 3.10+ terinstal.

```bash
# Install dependensi
pip install -r backend/requirements.txt

# Install Playwright browser
playwright install chromium

# Jalankan server
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 2. Frontend (React)
Pastikan Node.js 18+ terinstal.

```bash
# Install dependensi
npm install

# Jalankan dev server
npm run dev
```
Dashboard akan tersedia di `http://localhost:8080`. Frontend sudah dikonfigurasi untuk proxy ke backend di port 8000.

## 🧪 Verifikasi
Untuk memastikan sistem bekerja dengan benar, jalankan skrip integrasi:
```bash
python3 -m backend.test_organism
```

---
*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*
