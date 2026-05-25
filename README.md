<div align="center">

<a href="https://github.com/mulkymalikuldhrs/autonomous-organism">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=36&pause=1000&color=00D4AA&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=100&lines=Autonomous+Organism+v2.0" alt="Typing SVG" />
</a>

### 🧬 Self-Evolving Digital Organism — Sense, Think, Act, Evolve

[![Version](https://img.shields.io/badge/Version-2.0.0-00D4AA?style=for-the-badge)](./CHANGELOG.md)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite)](https://vitejs.dev/)
[![Supabase](https://img.shields.io/badge/Supabase-Backend-3ECF8E?style=for-the-badge&logo=supabase)](https://supabase.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/mulkymalikuldhrs/autonomous-organism?style=for-the-badge&logo=github)](https://github.com/mulkymalikuldhrs/autonomous-organism/stargazers)

</div>

---

## 🌐 Language / Bahasa / 语言

- 🇬🇧 [English](#-english) | 🇮🇩 [Bahasa Indonesia](#-bahasa-indonesia) | 🇨🇳 [中文](#-中文)

---

## 🇬🇧 English

### 🎯 About Autonomous Organism

Autonomous Organism is a self-evolving digital organism system that mimics biological life. It features a neural architecture with sense, decision, immune, memory, and factory subsystems — enabling it to perceive, think, act, and evolve autonomously. Built as a full-stack application with React frontend and Supabase backend.

### ✨ v2.0.0 — Production-Ready Release

This release transforms the project from a UI demo into a functional autonomous pipeline:

- 🔄 **Connected Pipeline**: Sense → Decision → Factory → Growth — all engines are wired to Supabase Edge Functions
- 🧠 **Decision Engine**: Real scoring with sentiment analysis, automation potential, and money potential; AI-enhanced via OpenAI API
- 🏭 **Factory Engine**: Generates SaaS project templates from top ideas; AI-enhanced page generation
- 📢 **Growth Engine**: Campaign generation and marketing simulation; AI-enhanced content creation
- 🗄️ **Real Database**: All metrics come from Supabase (problem_raw, idea_candidates, engine_runs, engine_logs)
- ⚙️ **Configurable AI Model**: Uses `gpt-4o-mini` by default, configurable via `VITE_AI_MODEL` env var
- 🛡️ **Fixed Hardcoded Paths**: All paths are relative (no more `/home/mulky/...`)
- 📊 **Real Dashboard**: Metrics pulled from actual Supabase queries, not simulation
- 🔧 **Fixed Config**: Package name, version, index.html title, ESLint — all corrected

### ✨ Key Features

- 🧠 **Neural Core Engine** — Central processing with real-time organism state visualization
- 👁️ **Sense Engine** — RSS + HackerNews ingestion via Supabase Edge Function
- ⚡ **Decision Engine** — Autonomous decision-making with heuristic + AI scoring
- 🛡️ **Immune System** — Self-healing and threat detection mechanisms
- 💾 **Memory System** — Persistent memory with learning capabilities
- 🏭 **Factory System** — SaaS template generation from validated ideas
- 📢 **Growth Engine** — Marketing campaign generation and user acquisition simulation
- 📊 **Scheduler** — Task scheduling and lifecycle management with guardrails
- 🤖 **AI Integration** — OpenAI API (edge functions) + Puter.js (client-side)
- 📈 **Real-time Dashboard** — Live organism metrics with animated visualizations
- 🔐 **Authentication** — Supabase Auth with org-based multi-tenancy

### 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                AUTONOMOUS ORGANISM v2.0                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  React   │  │  Vite    │  │Tailwind  │  │ Supabase │   │
│  │ Frontend │  │  Build   │  │  CSS 3   │  │ Backend  │   │
│  └────┬─────┘  └──────────┘  └──────────┘  └────┬─────┘   │
│       │                                           │          │
│  ┌────▼───────────────────────────────────────────▼──────┐  │
│  │           Supabase Edge Functions                     │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────────┐  │  │
│  │  │ingest- │ │run-    │ │run-    │ │run-          │  │  │
│  │  │sense   │ │decision│ │factory │ │growth        │  │  │
│  │  └────────┘ └────────┘ └────────┘ └──────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         AI Integration (OpenAI API / Puter.js)        │  │
│  │         Configurable via VITE_AI_MODEL env var        │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 🚀 Quick Start

```bash
git clone https://github.com/mulkymalikuldhrs/autonomous-organism.git
cd autonomous-organism
cp .env.example .env
# Edit .env with your Supabase credentials
npm install
npm run dev
```

### ⚙️ Environment Setup

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Run the migration in `supabase/migrations/`
3. Deploy the Edge Functions in `supabase/functions/`
4. Set the secrets in Supabase Dashboard (Edge Functions > Secrets):
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `SUPABASE_PUBLISHABLE_KEY`
   - `OPENAI_API_KEY` (optional — for AI-enhanced engines)
   - `AI_MODEL` (optional — default: `gpt-4o-mini`)

---

## 🇮🇩 Bahasa Indonesia

### 🎯 Tentang Autonomous Organism

Autonomous Organism adalah sistem organisme digital yang berevolusi sendiri yang meniru kehidupan biologis. Menampilkan arsitektur neural dengan subsistem indra, keputusan, kekebalan, memori, dan pabrik — memungkinkannya untuk merasakan, berpikir, bertindak, dan berevolusi secara otonom. Dibangun sebagai aplikasi full-stack dengan frontend React dan backend Supabase.

### ✨ v2.0.0 — Rilis Siap Produksi

Rilis ini mengubah proyek dari demo UI menjadi pipeline otonom yang fungsional:

- 🔄 **Pipeline Terhubung**: Sense → Decision → Factory → Growth — semua engine terhubung ke Supabase Edge Functions
- 🧠 **Decision Engine**: Scoring nyata dengan analisis sentimen, potensi otomatisasi, dan potensi uang; ditingkatkan AI via OpenAI API
- 🏭 **Factory Engine**: Menghasilkan template proyek SaaS dari ide terbaik; pembuatan halaman yang ditingkatkan AI
- 📢 **Growth Engine**: Pembuatan kampanye dan simulasi pemasaran; pembuatan konten yang ditingkatkan AI
- 🗄️ **Database Nyata**: Semua metrik berasal dari Supabase
- ⚙️ **Model AI Dikonfigurasi**: Menggunakan `gpt-4o-mini` secara default, dapat dikonfigurasi via env var `VITE_AI_MODEL`

### 🚀 Mulai Cepat

```bash
git clone https://github.com/mulkymalikuldhrs/autonomous-organism.git
cd autonomous-organism
cp .env.example .env
# Edit .env dengan kredensial Supabase Anda
npm install
npm run dev
```

---

## 🇨🇳 中文

### 🎯 关于 Autonomous Organism

Autonomous Organism 是一个模拟生物生命的自进化数字有机体系统。它具有感知、决策、免疫、记忆和工厂子系统的神经架构——使其能够自主感知、思考、行动和进化。使用 React 前端和 Supabase 后端构建的全栈应用程序。

### ✨ v2.0.0 — 生产就绪版本

此版本将项目从 UI 演示转变为功能性的自主管道：

- 🔄 **连接管道**: Sense → Decision → Factory → Growth — 所有引擎都连接到 Supabase Edge Functions
- 🧠 **决策引擎**: 真实评分，包含情感分析、自动化潜力和收益潜力；通过 OpenAI API 增强
- 🏭 **工厂引擎**: 从最佳创意生成 SaaS 项目模板；AI 增强页面生成
- 📢 **增长引擎**: 营销活动生成和模拟；AI 增强内容创建
- 🗄️ **真实数据库**: 所有指标来自 Supabase
- ⚙️ **可配置 AI 模型**: 默认使用 `gpt-4o-mini`，可通过 `VITE_AI_MODEL` 环境变量配置

### 🚀 快速开始

```bash
git clone https://github.com/mulkymalikuldhrs/autonomous-organism.git
cd autonomous-organism
cp .env.example .env
# 使用您的 Supabase 凭据编辑 .env
npm install
npm run dev
```

---

## 📦 Tech Stack

| Technology | Purpose | Version |
|-----------|---------|---------|
| React | Frontend UI | 18.x |
| TypeScript | Type Safety | 5.x |
| Vite | Build Tool | 5.x |
| Tailwind CSS | Styling | 3.x |
| shadcn/ui | UI Components | Latest |
| Supabase | Backend + Auth + Edge Functions | 2.x |
| OpenAI API | AI Engine (Edge Functions) | - |
| Puter.js | Client-side AI Fallback | - |
| Vitest | Testing | - |

---

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](./CONTRIBUTING.md) for details.

**Contact:** Mulky Malikul Dhaher | mulkymalikuldhaher@email.com

---

## ⚠️ Disclaimer

### 🇬🇧 English

> **⚠️ For Education Purpose Only**
> This project is provided strictly for educational and research purposes. The authors and contributors assume **no responsibility or liability** for any damages, losses, or risks arising from the use of this software. **We do not bear any responsibility or risk** for how this software is used.
> **Contact:** Mulky Malikul Dhaher | mulkymalikuldhaher@email.com

### 🇮🇩 Bahasa Indonesia

> **⚠️ Hanya untuk Tujuan Edukasi**
> Proyek ini disediakan secara ketat untuk tujuan edukasi dan penelitian. Penulis dan kontributor **tidak bertanggung jawab atau berkewajiban** atas kerusakan, kerugian, atau risiko yang timbul dari penggunaan perangkat lunak ini. **Kami tidak menanggung tanggung jawab atau risiko** apapun atas penggunaan perangkat lunak ini.
> **Kontak:** Mulky Malikul Dhaher | mulkymalikuldhaher@email.com

### 🇨🇳 中文

> **⚠️ 仅供教育目的**
> 本项目严格仅用于教育和研究目的。作者和贡献者对因使用本软件而产生的任何损害、损失或风险**不承担任何责任或义务**。**我们对本软件的使用方式不承担任何责任或风险**。
> **联系方式:** Mulky Malikul Dhaher | mulkymalikuldhaher@email.com

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by [Mulky Malikul Dhaher](https://github.com/mulkymalikuldhrs)**

⭐ If you find this project helpful, please give it a star!

</div>
