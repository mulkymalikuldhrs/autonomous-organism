# AGENTS.md - Organisme SaaS Otonom

## 🤖 Panduan Operasi Agent

Dokumen ini berisi instruksi khusus untuk agent (manusia atau AI) yang berinteraksi dengan codebase ini.

### 🧬 Etika Organisme
1.  **Jangan matikan siklus**: Organisme dirancang untuk hidup terus-menerus. Jika ingin melakukan perubahan besar, lakukan melalui penyesuaian bobot di `system_settings` atau modifikasi `Evolution Engine`.
2.  **Hargai kemandirian**: Hindari intervensi manual pada produk di direktori `products/` kecuali benar-benar diperlukan. Biarkan organisme belajar dari kegagalannya sendiri.
3.  **Prioritaskan Lokal**: Gunakan Ollama (Llama3) sebisa mungkin untuk menjaga kedaulatan data dan biaya rendah ($0).

### 🛠️ Pengaturan Organ
-   **Sense Engine**: Pastikan Playwright browser terinstal (`playwright install chromium`). Jika ingin menambah sumber, modifikasi `backend/engine/sense.py`.
-   **Decision Core**: Bobot awal disimpan di database SQLite (`organism.db`). Evolution Engine akan mengaturnya secara otomatis seiring waktu.
-   **Monetization Engine**: Simulasi pendapatan saat ini didasarkan pada metrik trafik. Hubungkan ke API pembayaran nyata (Stripe/Xendit) di Gen-5 untuk pendapatan nyata.

### 🧪 Prosedur Pengujian
Selalu jalankan tes integrasi sebelum melakukan commit besar:
```bash
python3 -m backend.test_organism
```
Pastikan `backend.log` dan `frontend.log` tidak menunjukkan error fatal.

### 📈 Evolusi
Organisme ini "belajar" dengan cara:
1. Mencatat `RevenueLog` dan `TrafficLog`.
2. `Evolution Engine` membaca log tersebut.
3. Menyesuaikan `decision_revenue_weight`, `decision_neg_weight`, dll.
4. `Decision Core` menggunakan bobot baru untuk memilih ide berikutnya.

---
*"Bukan membangun produk, tapi membangun sistem yang membangun produk."*
