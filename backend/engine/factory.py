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
'db_schema': [list of SQL tables and columns with data types]
'endpoints': [list of FastAPI endpoints with methods and descriptions]
'features': [list of key features]
'ui_ux_strategy': "Detailed UI design approach"
'monetization_model': "Specific revenue strategy"
'stack': {{'backend': 'FastAPI', 'frontend': 'React/Vite/Tailwind', 'db': 'SQLite'}}
"""
    spec_raw = await llm.generate(prompt, system="You are the SaaS Architect.")

    try:
        json_match = re.search(r"(\{.*\})", spec_raw, re.S)
        spec = json.loads(json_match.group(1)) if json_match else {"raw": spec_raw}
    except:
        spec = {"raw": spec_raw}

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

      <nav className="w-full max-w-6xl flex justify-between items-center mb-16 backdrop-blur-md bg-slate-900/50 p-6 rounded-2xl border border-slate-800 shadow-2xl shadow-cyan-500/5">
        <div className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent tracking-tighter">
          {top_idea.theme.upper()}
        </div>
        <div className="flex gap-8 text-xs font-bold uppercase tracking-widest text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Features</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Neural Network</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Monetization</a>
        </div>
      </nav>

      <main className="w-full max-w-6xl flex flex-col items-center text-center">
        <div className="inline-block px-4 py-1.5 mb-6 rounded-full border border-cyan-500/20 bg-cyan-500/5 text-cyan-400 text-[10px] font-black uppercase tracking-[0.2em] animate-pulse">
          Autonomous Species Output: GEN-4.1
        </div>

        <h1 className="text-6xl md:text-8xl font-black text-white mb-8 tracking-tighter leading-none">
          SYSTEM <span className="bg-gradient-to-b from-cyan-300 to-cyan-600 bg-clip-text text-transparent">{top_idea.theme.upper()}</span>
        </h1>

        <p className="text-slate-400 text-xl max-w-3xl mb-16 leading-relaxed font-light">
          {top_idea.summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-8 mb-24">
          {{ {json.dumps(spec.get('features', []))}.map((f, i) => (
            <div key={{i}} className="group relative bg-slate-900/40 p-8 rounded-3xl border border-slate-800 hover:border-cyan-500/50 transition-all duration-500 hover:-translate-y-2">
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-3xl" />
              <div className="relative z-10">
                <div className="w-12 h-12 bg-slate-800 text-cyan-400 rounded-xl flex items-center justify-center mb-6 font-black text-xl border border-slate-700 group-hover:scale-110 transition-transform">
                  0{{i + 1}}
                </div>
                <h3 className="font-bold text-white text-xl mb-3 text-left tracking-tight">{{f}}</h3>
                <p className="text-slate-500 text-sm text-left leading-relaxed">Generated by the SAAS Factory rahim using autonomous architectural blueprints.</p>
              </div>
            </div>
          )) }}
        </div>

        <div className="relative group w-full max-w-4xl">
          <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-violet-600 rounded-[2rem] blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200" />
          <div className="relative bg-slate-900 rounded-[2rem] p-12 border border-slate-800 flex flex-col items-center">
            <h2 className="text-4xl font-black text-white mb-4 tracking-tight">INITIALIZE CONNECTION</h2>
            <p className="text-slate-400 mb-10 max-w-md font-medium">Join the decentralized autonomous network of {top_idea.theme}.</p>

            <div className="flex w-full max-w-md gap-3 p-2 bg-slate-950 rounded-2xl border border-slate-800 shadow-inner">
              <input
                type="email"
                placeholder="NEURAL_ID@HOST.COM"
                className="flex-1 bg-transparent px-4 py-3 rounded-xl text-cyan-400 placeholder:text-slate-700 focus:outline-none font-mono text-sm"
              />
              <button className="px-8 py-3 bg-cyan-500 text-slate-950 font-black rounded-xl hover:bg-cyan-400 transition-all active:scale-95 shadow-lg shadow-cyan-500/20 uppercase tracking-tighter">
                Access
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-32 border-t border-slate-900 w-full pt-12 pb-12 flex flex-col items-center gap-4">
        <div className="flex gap-8 text-slate-600 text-[10px] font-bold uppercase tracking-[0.3em]">
          <span>Status: Operational</span>
          <span>Gen: 4.1</span>
          <span>Target: $50K/MO</span>
        </div>
        <div className="text-slate-700 text-[9px] font-mono">
          &copy; {{new Date().getFullYear()}} {top_idea.theme.upper()} // BUILT BY THE ORGANISM
        </div>
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
      - "8080:80"
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
