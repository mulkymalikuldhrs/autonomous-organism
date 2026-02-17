# ORGANISME SAAS OTONOM (Gen-3)

## Blueprint Teknis – Gratis, Open Source, Otonom

Sistem ini adalah **Organisme SaaS Otonom** yang dirancang untuk menemukan masalah manusia, membangun solusi, melakukan pemasaran, dan berevolusi secara mandiri.

### Fitur Utama (Gen-3)
- **Sense Engine (Indra):** Scraper real-time untuk Hacker News, Reddit (SaaS, Startups, Entrepreneur, SideProject), dan IndieHackers RSS.
- **Decision Core (Otak):** Clustering masalah menggunakan TF-IDF & K-Means, analisis sentimen VADER, dan scoring dinamis.
- **SaaS Factory (Rahim):** Generator otomatis yang membangun struktur folder produk (FastAPI Backend + HTML/Tailwind Frontend) di direktori `products/`.
- **Growth Engine (Mulut):** Pembuat konten pemasaran otomatis untuk Twitter, Reddit, IndieHackers, dan Medium di `growth_outbox/`.
- **Evolution Engine (Evolusi):** Tuning bobot scoring secara otomatis berdasarkan data performa (`RevenueLog` & `TrafficLog`).
- **Agent Spawner:** Manajemen siklus hidup sub-agent spesialis untuk setiap produk yang dibangun.
- **Immune System:** Pemantauan kesehatan sistem dan isolasi otomatis jika terjadi error berlebih.

### Tech Stack
- **Frontend:** React, Vite, TypeScript, Tailwind CSS, shadcn-ui.
- **Backend:** FastAPI, SQLAlchemy, SQLite.
- **AI/LLM:** Local Ollama (llama3) atau HuggingFace Free Inference API (Mistral-7B).
- **Data Science:** scikit-learn, NLTK, Pandas.

### Cara Menjalankan
1. **Frontend Setup:**
   ```bash
   npm i
   npm run dev
   ```
2. **Backend Setup:**
   ```bash
   pip install -r backend/requirements.txt
   uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```
3. **Konfigurasi (Opsional):**
   - Tambahkan `HF_TOKEN` di `.env` untuk menggunakan HuggingFace.
   - Pastikan Ollama jalan di `localhost:11434` untuk mode lokal penuh.

### Filosofi
"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."
Sistem ini tidak membutuhkan intervensi manusia untuk siklus hidup harian. Ia akan terus mencari peluang, membangun MVP, dan mencoba tumbuh sendiri.
