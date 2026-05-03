from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import json
import re

async def run_factory(db: Session):
    log = models.EngineLog(level="info", source="Factory", message="SaaS Factory started (Gen-4 Enhanced Build)")
    db.add(log)
    db.commit()

    # Get top unprocessed idea
    top_idea = db.query(models.IdeaCandidate).filter(models.IdeaCandidate.is_processed == False).order_by(models.IdeaCandidate.score.desc()).first()
    if not top_idea:
        db.add(models.EngineLog(level="info", source="Factory", message="No new ideas to build."))
        db.commit()
        return

    # 1. Brainstorming Complete Spec
    prompt = f"""Generate a full technical specification for a SaaS MVP:
Idea: {top_idea.theme}
Summary: {top_idea.summary}

Output JSON with keys:
'db_schema': [list of SQL tables and columns]
'endpoints': [list of FastAPI endpoints with methods]
'features': [list of key features]
'ui_ux_strategy': 'Detailed UI/UX strategy for bioluminescent theme'
'monetization_model': 'Detailed monetization plan'
'stack': {{'backend': 'FastAPI', 'frontend': 'React/Vite/Tailwind', 'db': 'SQLite'}}
"""
    spec_raw = await llm.generate(prompt, system="You are the SaaS Architect.")

    try:
        # Robust JSON extraction
        json_match = re.search(r"(\{.*\})", spec_raw, re.S)
        if json_match:
            clean_json = json_match.group(1).replace("'", "\"")
            spec = json.loads(clean_json)
        else:
            spec = {"raw": spec_raw}
    except Exception as e:
        print(f"Error parsing JSON in SaaS Factory: {e}")
        spec = {"raw": spec_raw, "features": ["MVP Feature 1", "MVP Feature 2"]}

    os.makedirs("products", exist_ok=True)
    product_name = top_idea.theme.lower().replace(" ", "_").replace("/", "_")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    product_dir = f"products/{product_name}_{timestamp}"
    os.makedirs(product_dir, exist_ok=True)

    # 2. Generate Files
    # A. backend/main.py
    backend_dir = f"{product_dir}/backend"
    os.makedirs(backend_dir, exist_ok=True)
    with open(f"{backend_dir}/main.py", "w") as f:
        f.write(f"""from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="{top_idea.theme} API")

@app.get("/")
def read_root():
    return {{"status": "online", "name": "{top_idea.theme}"}}

@app.get("/api/features")
def get_features():
    return {json.dumps(spec.get('features', []))}

@app.get("/health")
def health():
    return {{"status": "healthy"}}
""")

    # B. frontend/ (React Skeleton with Tailwind)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)
    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write(f"""
import React from 'react';

function App() {{
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-8 font-sans selection:bg-cyan-500/30">
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(17,24,39,1),rgba(2,6,23,1))] -z-10" />

      <nav className="w-full max-w-5xl flex justify-between items-center mb-16 backdrop-blur-md bg-slate-900/50 p-6 rounded-2xl border border-slate-800/50 shadow-xl shadow-cyan-500/5">
        <div className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent tracking-tighter uppercase">{top_idea.theme}</div>
        <div className="flex gap-8 text-sm font-bold uppercase tracking-widest text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Neural Sync</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Core Specs</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Nodes</a>
        </div>
      </nav>

      <main className="w-full max-w-5xl flex flex-col items-center text-center">
        <div className="inline-block px-4 py-1.5 mb-6 text-[10px] font-bold tracking-[0.2em] uppercase bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded-full shadow-[0_0_15px_rgba(34,211,238,0.1)]">
          Autonomous Species v4.1 Detected
        </div>

        <h1 className="text-6xl md:text-8xl font-black text-white mb-8 leading-none tracking-tight">
          Evolution of <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-600 bg-clip-text text-transparent">{top_idea.theme}</span>
        </h1>

        <p className="text-slate-400 text-xl max-w-3xl mb-12 leading-relaxed font-light">
          {top_idea.summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          {{ {json.dumps(spec.get('features', []))}.map((f, i) => (
            <div key={{i}} className="group bg-slate-900/40 p-8 rounded-3xl border border-slate-800/50 hover:border-cyan-500/50 hover:bg-slate-900/60 transition-all duration-500 hover:shadow-[0_0_30px_rgba(34,211,238,0.05)] text-left">
              <div className="w-12 h-12 bg-gradient-to-br from-cyan-500 to-blue-600 text-white rounded-xl flex items-center justify-center mb-6 font-black shadow-lg shadow-cyan-500/20 group-hover:scale-110 transition-transform">
                {{String(i + 1).padStart(2, '0')}}
              </div>
              <h3 className="font-bold text-white text-xl mb-3 tracking-tight group-hover:text-cyan-400 transition-colors">{{f}}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">Neural-optimized autonomous module configured for high-frequency human problem resolution.</p>
            </div>
          )) }}
        </div>

        <div className="relative group w-full max-w-4xl">
          <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-violet-600 rounded-[2rem] blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
          <div className="relative bg-slate-900 border border-slate-800 rounded-[2rem] p-12 w-full flex flex-col items-center shadow-2xl">
            <h2 className="text-4xl font-black text-white mb-4">Initialize Connection</h2>
            <p className="text-slate-400 mb-10 max-w-md">Synchronize with {top_idea.theme} neural network and scale your operational efficiency.</p>
            <div className="flex w-full max-w-md gap-3 p-2 bg-slate-950 rounded-2xl border border-slate-800 focus-within:border-cyan-500/50 transition-colors">
              <input type="email" placeholder="NEURAL_ID@HOST.SYS" className="flex-1 bg-transparent px-4 py-3 text-white placeholder:text-slate-700 focus:outline-none font-mono text-sm" />
              <button className="px-8 py-3 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black rounded-xl transition-all active:scale-95 shadow-lg shadow-cyan-500/20">
                SYNC
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-24 text-slate-600 text-[10px] font-bold tracking-[0.3em] uppercase pb-12">
        [ &copy; {{new Date().getFullYear()}} {top_idea.theme} // POWERED BY ORGANISME SAAS OTONOM ]
      </footer>
    </div>
  );
}}
export default App;
""")

    # C. Dockerfile
    with open(f"{product_dir}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
""")

    # D. docker-compose.yml
    with open(f"{product_dir}/docker-compose.yml", "w") as f:
        f.write(f"""version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8081:80"
""")

    # E. requirements.txt
    with open(f"{backend_dir}/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn\npydantic\n")

    # Create product record
    blueprint_path = f"{product_dir}/blueprint.json"
    with open(blueprint_path, "w") as f:
        json.dump({"idea_id": top_idea.id, "spec": spec}, f, indent=2)

    new_product = models.Product(
        idea_id=top_idea.id,
        name=top_idea.theme,
        blueprint_path=blueprint_path
    )
    db.add(new_product)

    # Mark idea as processed
    top_idea.is_processed = True

    db.add(models.EngineLog(level="success", source="Factory", message=f"Full SaaS structure generated for: {top_idea.theme}"))
    db.commit()
    return {"product": top_idea.theme, "path": product_dir}
