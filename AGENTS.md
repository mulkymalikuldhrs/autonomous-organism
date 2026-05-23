# 🤖 AUTONOMOUS AGENTS (GEN-4)

This document describes the operational roles and life-cycles of the autonomous agents within the **ORGANISME SAAS OTONOM**.

---

## 1. CORE ARCHITECTURE (8-STAGE LIFECYCLE)

The organism operates on a continuous loop, executing 8 distinct stages that simulate the behavior of a living digital species.

1.  **👁️ SENSE**: Scans sources (HackerNews, Reddit RSS, ProductHunt) using Playwright and BS4 to find human problems.
2.  **🧠 DECISION**: Analyzes and scores findings using NLTK sentiment analysis and LLM strategic evaluation.
3.  **🏭 FACTORY**: Generates full-stack React + FastAPI code for top ideas and stores them in the `products/` directory.
4.  **🧬 SPAWNER**: Maintains a fleet of sub-agents (Builder, Growth, Support) to handle specific tasks.
5.  **📢 GROWTH**: Creates and logs multi-stage marketing campaigns (Pre-Launch to Post-Launch) for built products.
6.  **💰 MONETIZATION**: Simulates and tracks revenue generated through various models (Affiliate, SaaS Subscriptions, etc.).
7.  **🔄 EVOLUTION**: Adjusts internal scoring weights and strategies based on revenue and traffic performance.
8.  **🛡️ IMMUNE**: Monitors system vitals (error rates, disk space, runaway processes) and self-terminates if unsafe.

---

## 2. AGENT TYPES

| Agent Type | Personality | Mission |
|------------|-------------|---------|
| **Research** | Analytical | Identify deep market gaps and persistent human pain points. |
| **Builder** | Efficient | Generate clean, functional, and production-ready code for MVP solutions. |
| **Growth** | Creative | Craft compelling narratives and campaigns to attract early adopters. |
| **Support** | Persistent | Maintain existing products and handle simulated user feedback. |

---

## 3. OPERATIONAL RULES

- **ZERO COST**: Agents must prioritize local resources (Ollama) and free tiers over paid APIs.
- **SUICIDE CLAUSE**: If the organism detects harm to the owner's reputation or finances, it will trigger an immediate shutdown.
- **SELF-EVOLUTION**: No human intervention is required for strategy updates; the organism learns from its own `life_log`.

---

## 4. VERIFICATION

To verify the operation of the agents:

1.  Check the `organism.db` (SQLite) for entries in `agent_status` and `engine_logs`.
2.  Monitor the **Dashboard** at `http://localhost:8080` for real-time vital signs.
3.  Run the verification script: `python3 verify_organism_ui.py`.
