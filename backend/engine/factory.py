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
'ui_ux_strategy': <string describing the strategy>
'monetization_model': <string describing the model>
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

    # B. frontend/ (React Skeleton with Bioluminescent Edition Design)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)
    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write(f"""
import React from 'react';

function App() {{
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-8 font-sans">
      <nav className="w-full max-w-4xl flex justify-between items-center mb-12 border-b border-slate-800 pb-4">
        <div className="text-2xl font-bold text-cyan-400 tracking-tighter drop-shadow-[0_0_8px_rgba(34,211,238,0.8)]">{top_idea.theme.upper()}</div>
        <div className="flex gap-6 text-xs font-mono uppercase tracking-widest text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Features</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Neural Network</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Connect</a>
        </div>
      </nav>

      <main className="w-full max-w-4xl flex flex-col items-center text-center">
        <div className="inline-block px-3 py-1 rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-400 text-[10px] font-mono mb-6 animate-pulse">
          AUTONOMOUS GEN-4 SYSTEM ACTIVE
        </div>
        <h1 className="text-5xl md:text-7xl font-black text-white mb-6 leading-none tracking-tight">
          THE <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-500">{top_idea.theme.upper()}</span> PROTOCOL
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mb-12 leading-relaxed font-light">
          {top_idea.summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {{ {json.dumps(spec.get('features', []))}.map((f, i) => (
            <div key={{i}} className="group relative bg-slate-900/50 p-8 rounded-3xl border border-slate-800 hover:border-cyan-500/50 transition-all duration-500 overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="text-cyan-500 font-mono text-xs mb-4 opacity-50">0{{i + 1}} // MODULE</div>
              <h3 className="font-bold text-white text-xl mb-3 text-left tracking-tight group-hover:text-cyan-400 transition-colors">{{f}}</h3>
              <p className="text-slate-500 text-sm text-left leading-relaxed">Neural-optimized deployment of the {top_idea.theme} core subsystem.</p>
            </div>
          )) }}
        </div>

        <div className="relative group bg-slate-900 rounded-[2rem] p-12 w-full flex flex-col items-center border border-slate-800 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 via-transparent to-violet-500/5"></div>
          <h2 className="text-3xl font-bold text-white mb-4 relative z-10">INITIALIZE CONNECTION</h2>
          <p className="text-slate-400 mb-10 max-w-md relative z-10 font-light">Join the evolution. Enter your neural address to receive {top_idea.theme} updates.</p>
          <div className="flex w-full max-w-sm gap-3 relative z-10">
            <input type="email" placeholder="NEURAL_ID@DOMAIN" className="flex-1 bg-slate-950 border border-slate-800 px-5 py-4 rounded-2xl text-white focus:outline-none focus:border-cyan-500/50 transition-all placeholder:text-slate-700 font-mono text-sm" />
            <button className="px-8 py-4 bg-cyan-500 text-slate-950 font-black rounded-2xl hover:bg-cyan-400 transition-all hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(34,211,238,0.3)]">
              JOIN
            </button>
          </div>
        </div>
      </main>

      <footer className="mt-20 text-slate-600 text-[10px] font-mono tracking-widest pb-12 uppercase">
        &copy; {{new Date().getFullYear()}} {top_idea.theme} // ORGANISME SAAS OTONOM // ALL RIGHTS RESERVED
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
