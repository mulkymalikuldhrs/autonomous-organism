# 🧬 BLUEPRINT TEKNIS: ORGANISME SAAS OTONOM (GEN-4)

## Misi: $50,000/bulan dalam 12 bulan

---

## 0. TUJUAN HIDUP

Sistem otonom yang mandiri (self-sustaining digital species) yang secara terus-menerus:
1.  **Menemukan masalah** dari sumber data publik (Reddit, Kaskus, dll.).
2.  **Memilih masalah** dengan skor potensi pendapatan tertinggi.
3.  **Membangun solusi** MVP (SaaS) secara otomatis.
4.  **Deploy otomatis** menggunakan platform gratis (Vercel, Oracle Cloud).
5.  **Mencari user** lewat channel marketing otomatis.
6.  **Menghasilkan uang** (Revenue) untuk membiayai operasinya sendiri.
7.  **Evaluasi performa** (Pola gagal/sukses).
8.  **Upgrade diri** (Evolution Engine) untuk efisiensi lebih tinggi.
9.  **Melahirkan agent** atau organisme baru jika target tercapai.

---

## 1. ATURAN OPERASIONAL

- **Tanpa API berbayar:** Prioritaskan LLM lokal (Ollama) dan HuggingFace free inference.
- **Tanpa vendor mahal:** Gunakan free tiers dan PC lokal.
- **Open source:** Transparansi kode dan logika.
- **Bisa bunuh diri (Suicide):** Jika sistem merugikan pemilik atau melanggar aturan moral/finansial.

---

## 2. ARSITEKTUR SISTEM (GEN-4)

### A. SENSE ENGINE (INDRA)
- **Teknologi:** Playwright (Headless Browser), BeautifulSoup, LXML.
- **Sumber Data:** Reddit (r/indonesia, r/startups), Kaskus, Quora, Youtube Comments, Marketplace Reviews.
- **Logika:** Scrape, de-noise (LLM Filter), dan simpan ke `problem_raw`.

### B. DECISION CORE (OTAK)
- **Teknologi:** NLTK (VADER Sentiment), Scikit-learn (KMeans/TF-IDF).
- **Formula Skor:**
  `score = (keluhan * 0.4) + (emosi_negatif * 0.2) + (mudah_otomatis * 0.2) + (potensi_uang * 0.2)`
- **Output:** Menyimpan kandidat ide ke `idea_candidates`.

### C. SAAS FACTORY (RAHIM)
- **Teknologi:** FastAPI (Backend), React/Tailwind (Frontend), Docker.
- **Proses:** LLM men-generate blueprint, skema DB, dan endpoint API.
- **Output:** Folder produk di `products/` dengan `docker-compose.yml`.

### D. GROWTH ENGINE (MULUT)
- **Teknologi:** LLM (Content Gen), Web Scraper (Market Research).
- **Proses:** Posting ke forum, blog otomatis, dan tracking signups.

### E. MONETIZATION ENGINE (PERUT)
- **Model:** Affiliate, Subscription, Lead Gen, Donations.
- **Tracking:** Mencatat pendapatan ke `revenue_log`.

### F. MEMORY ENGINE (INGATAN)
- **Penyimpanan:** SQLite (`organism.db`).
- **Analisis:** Mengumpulkan `EngineLog` dan `LifeLog` untuk belajar dari kegagalan.

### G. IMMUNE SYSTEM (ANTI-GILA)
- **Batas Keras:** Timeout eksekusi, limit penggunaan disk, limit error rate.
- **Tindakan:** Mematikan sub-agent (kill-switch) jika loop atau boros resource.

### H. EVOLUTION (PENINGKATAN)
- **Dinamis:** Menyesuaikan bobot formula scoring berdasarkan produk yang menghasilkan revenue tertinggi.
- **Upgrade:** Memperbarui prompt LLM secara otomatis.

---

## 3. STRUKTUR DATABASE (`organism.db`)

1.  **problem_raw:** Data mentah dari web.
2.  **problem_clean:** Masalah yang sudah dibersihkan.
3.  **idea_candidates:** Skor dan Blueprint ide.
4.  **products:** Daftar produk yang sudah dibangun.
5.  **engine_logs:** Saraf sistem (monitoring).
6.  **revenue_log:** Data finansial.
7.  **system_settings:** Parameter dinamis untuk evolusi.

---

## 4. PERAN PEMILIK

Pemilik tidak mengoperasikan sistem harian. Pemilik hanya:
- Menetapkan Nilai Hidup (Moral & Finansial).
- Memantau Dashboard Visual.
- Melakukan Kill-Switch jika diperlukan.

*"Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."*
