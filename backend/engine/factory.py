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

    # B. frontend/ (React Skeleton with Bioluminescent Edition UI)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)

    features_json = json.dumps(spec.get('features', []))
    ui_code = f"""
import React from 'react';

function App() {{
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-8 font-sans selection:bg-cyan-500/30">
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(17,24,39,1),rgba(2,6,23,1))] -z-10" />
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-6xl h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent shadow-[0_0_20px_rgba(6,182,212,0.5)]" />

      <nav className="w-full max-w-5xl flex justify-between items-center mb-20 backdrop-blur-sm bg-slate-950/50 p-4 rounded-2xl border border-slate-800/50">
        <div className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent tracking-tighter italic">
          {top_idea.theme.upper()}
        </div>
        <div className="flex gap-8 text-xs font-bold uppercase tracking-widest text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Features</a>
          <a href="#" className="hover:text-violet-400 transition-colors">Pricing</a>
          <button className="px-4 py-1.5 rounded-full border border-cyan-500/30 text-cyan-400 hover:bg-cyan-500/10 transition-all">
            Connect
          </button>
        </div>
      </nav>

      <main className="w-full max-w-4xl flex flex-col items-center text-center">
        <div className="inline-block px-3 py-1 rounded-full border border-cyan-500/20 bg-cyan-500/5 text-cyan-400 text-[10px] font-bold uppercase tracking-[0.2em] mb-6">
          Gen-4 Autonomous Solution
        </div>

        <h1 className="text-6xl md:text-7xl font-black text-white mb-8 leading-[0.9] tracking-tighter">
          SOLVING <span className="bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent">{top_idea.theme.upper()}</span> AT SCALE.
        </h1>

        <p className="text-slate-400 text-lg max-w-2xl mb-12 leading-relaxed font-medium">
          {top_idea.summary}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full mb-20">
          {{ {features_json}.map((f, i) => (
            <div key={{i}} className="group bg-slate-900/40 p-8 rounded-3xl border border-slate-800 hover:border-cyan-500/30 transition-all duration-500 text-left relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-cyan-500 to-violet-500 opacity-0 group-hover:opacity-100 transition-opacity" />
              <div className="text-3xl font-black text-slate-800 mb-4 group-hover:text-cyan-500/20 transition-colors">
                0{{i + 1}}
              </div>
              <h3 className="font-bold text-white text-xl mb-3 tracking-tight">{{f}}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">
                Autonomous system capability refined through genetic evolution and market-fit analysis.
              </p>
            </div>
          )) }}
        </div>

        <div className="relative group w-full max-w-2xl">
          <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-violet-600 rounded-[2rem] blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
          <div className="relative bg-slate-950 rounded-[2rem] p-12 border border-slate-800 flex flex-col items-center">
            <h2 className="text-3xl font-black text-white mb-4 italic tracking-tight">ENLIST IN THE EVOLUTION</h2>
            <p className="text-slate-400 mb-8 text-sm font-medium tracking-wide">Join 2,500+ operators utilizing autonomous infrastructure.</p>
            <div className="flex w-full max-w-md gap-3 p-1.5 bg-slate-900 rounded-2xl border border-slate-800 focus-within:border-cyan-500/50 transition-colors">
              <input
                type="email"
                placeholder="OPERATOR EMAIL"
                className="flex-1 bg-transparent px-4 py-2 text-white text-xs font-bold uppercase tracking-widest focus:outline-none placeholder:text-slate-600"
              />
              <button className="px-8 py-3 bg-white text-slate-950 text-xs font-black uppercase tracking-widest rounded-xl hover:bg-cyan-400 transition-colors">
                Initialize
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-32 text-slate-600 text-[10px] font-bold uppercase tracking-[0.3em] pb-12 flex flex-col items-center gap-4">
        <div className="w-12 h-px bg-slate-800" />
        <div>&copy; {{new Date().getFullYear()}} {top_idea.theme.upper()} // ORGANISME SAAS OTONOM // ALL RIGHTS RESERVED</div>
      </footer>
    </div>
  );
}}
export default App;
"""
    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write(ui_code)

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
