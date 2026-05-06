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

    # 1. Brainstorming Complete Spec (Gen-4.1)
    prompt = f"""Generate a full technical specification for a SaaS MVP:
Idea: {top_idea.theme}
Summary: {top_idea.summary}

Output JSON with keys:
'db_schema': [list of SQL tables and columns]
'endpoints': [list of FastAPI endpoints with methods]
'features': [list of key features]
'ui_ux_strategy': "Detailed UI/UX approach"
'monetization_model': "How this product will make money"
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

    # B. frontend/ (React Bioluminescent Edition)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)
    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write(f"""
import React from 'react';

function App() {{
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-8 font-sans selection:bg-cyan-500/30">
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(17,24,39,1),rgba(2,6,23,1))] -z-10" />
      <div className="fixed top-0 left-0 w-full h-1 bg-gradient-to-r from-cyan-500 via-violet-500 to-fuchsia-500 opacity-50" />

      <nav className="w-full max-w-5xl flex justify-between items-center mb-16 backdrop-blur-md bg-slate-900/50 p-6 rounded-2xl border border-slate-800/50 shadow-2xl shadow-cyan-500/5">
        <div className="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-400 tracking-tighter uppercase italic">
          {top_idea.theme}
        </div>
        <div className="flex gap-8 text-xs font-bold uppercase tracking-widest text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Intelligence</a>
          <a href="#" className="hover:text-violet-400 transition-colors">Nexus</a>
          <a href="#" className="hover:text-fuchsia-400 transition-colors">Contact</a>
        </div>
      </nav>

      <main className="w-full max-w-5xl flex flex-col items-center text-center">
        <div className="inline-block px-4 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-[10px] font-black uppercase tracking-[0.2em] mb-8 animate-pulse">
          Autonomous Solution Gen-4.1
        </div>

        <h1 className="text-6xl md:text-8xl font-black text-white mb-8 tracking-tighter leading-none">
          THE <span className="bg-clip-text text-transparent bg-gradient-to-b from-white to-slate-500">{top_idea.theme.upper()}</span> NEXUS
        </h1>

        <p className="text-slate-400 text-lg md:text-xl max-w-3xl mb-12 leading-relaxed font-light">
          {top_idea.summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          {{ {json.dumps(spec.get('features', []))}.map((f, i) => (
            <div key={{i}} className="group relative bg-slate-900/40 p-8 rounded-3xl border border-slate-800/50 hover:border-cyan-500/50 transition-all duration-500 hover:translate-y-[-4px]">
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-violet-500/5 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity" />
              <div className="relative z-10">
                <div className="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center mb-6 border border-slate-700 group-hover:border-cyan-500/50 group-hover:shadow-[0_0_20px_rgba(6,182,212,0.3)] transition-all">
                  <span className="text-cyan-400 font-black">0{{i + 1}}</span>
                </div>
                <h3 className="font-bold text-white text-xl mb-3 text-left tracking-tight">{{f}}</h3>
                <p className="text-slate-500 text-sm text-left leading-relaxed">Neural-optimized autonomous module designed for peak performance.</p>
              </div>
            </div>
          )) }}
        </div>

        <div className="relative w-full max-w-4xl p-[1px] rounded-[40px] bg-gradient-to-r from-cyan-500 via-violet-500 to-fuchsia-500 overflow-hidden shadow-2xl shadow-cyan-500/20">
          <div className="bg-slate-950 rounded-[39px] p-12 md:p-16 flex flex-col items-center relative overflow-hidden">
             <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 blur-[100px] -mr-32 -mt-32" />
             <div className="absolute bottom-0 left-0 w-64 h-64 bg-violet-500/10 blur-[100px] -ml-32 -mb-32" />

            <h2 className="text-4xl md:text-5xl font-black text-white mb-6 tracking-tight">Initiate Integration</h2>
            <p className="text-slate-400 mb-10 max-w-md text-lg">Deploy the {top_idea.theme} autonomous intelligence to your workflow today.</p>

            <div className="flex flex-col sm:flex-row w-full max-w-md gap-3">
              <input
                type="email"
                placeholder="ACCESS_EMAIL@PROTOCOL"
                className="flex-1 px-6 py-4 rounded-2xl bg-slate-900 border border-slate-800 text-white focus:outline-none focus:border-cyan-500 transition-colors font-mono text-sm"
              />
              <button className="px-8 py-4 bg-white text-black font-black rounded-2xl hover:bg-cyan-400 transition-all active:scale-95 shadow-xl shadow-white/10 uppercase text-xs tracking-widest">
                Authorize
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-24 text-slate-600 text-[10px] pb-12 font-bold uppercase tracking-[0.3em]">
        &copy; {{new Date().getFullYear()}} {top_idea.theme} &bull; Autonomous Organism Gen-4.1 &bull; System Online
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

    # D. docker-compose.yml (Port 8081 for products)
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
