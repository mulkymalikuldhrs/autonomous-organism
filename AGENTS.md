# ORGANISME SAAS OTONOM - Agent Protocol

This repository contains the source code for a self-evolving SaaS organism.

## Architecture

- **Frontend**: Vite + React + Tailwind (Root)
- **Backend**: FastAPI + SQLAlchemy + SQLite (`/backend`)
- **Intelligence**: Scikit-Learn (Clustering), NLTK (Sentiment), LLM Fallback Pipeline.

## Engines

1.  **Sense Engine (Indra)**: Scrapes HackerNews and Reddit for human problems.
2.  **Decision Core (Otak)**: Clusters problems using TF-IDF/KMeans and scores them based on volume and sentiment.
3.  **SaaS Factory (Rahim)**: Scaffolds product blueprints and documentation in `/products`.
4.  **Growth Engine (Mulut)**: Generates promotional content and logs to `/growth_outbox`.
5.  **Monetization Engine (Perut)**: Simulates revenue tracking and affiliate optimization.
6.  **Immune System**: Monitors system health and failure rates.

## Setup & Operation

### Local Development
1.  **Frontend**: `npm install && npm run dev`
2.  **Backend**:
    - `pip install -r backend/requirements.txt`
    - `export PYTHONPATH=$PYTHONPATH:.`
    - `python -m uvicorn backend.main:app --reload`

### Autonomous Mode
The backend includes a `run_lifecycle_loop` that automatically executes all engines every 10 minutes.

## Guardrails
- **Kill Switch**: Can be implemented by stopping the backend process.
- **Immune System**: Will flag critical failures in the logs if the error threshold is exceeded.

## Evolution
The system is designed to be modified by its own `Factory` engine. Future iterations should allow the `Factory` to commit code changes back to the repository.
