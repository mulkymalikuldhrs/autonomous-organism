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
    prompt = f"""Generate a comprehensive technical blueprint for a SaaS MVP:
Idea: {top_idea.theme}
Summary: {top_idea.summary}

The blueprint must include:
1. Detailed Database Schema (SQLAlchemy models)
2. REST API Endpoints (FastAPI)
3. UI/UX Strategy (Bioluminescent design theme: dark slate-950 background, cyan-400 accents, violet-500 secondary)
4. Key MVP Features
5. Monetization Strategy (Affiliate, Subscription, or Credits)

Output JSON with keys:
'db_schema': [list of SQL tables and columns]
'endpoints': [list of FastAPI endpoints with methods]
'features': [list of key features]
'ux_strategy': 'string description'
'monetization': 'string description'
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
      <nav className="w-full max-w-4xl flex justify-between items-center mb-12 border-b border-slate-800 pb-6">
        <div className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent tracking-tighter">{top_idea.theme.upper()}</div>
        <div className="flex gap-6 text-xs font-mono uppercase tracking-widest text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">System</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Protocol</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Access</a>
        </div>
      </nav>

      <main className="w-full max-w-4xl flex flex-col items-center text-center">
        <div className="inline-block px-3 py-1 rounded-full border border-cyan-500/30 bg-cyan-500/5 text-cyan-400 text-[10px] font-mono uppercase mb-6 animate-pulse">
          Autonomous Solution Online
        </div>
        <h1 className="text-5xl md:text-7xl font-black text-white mb-6 leading-tight tracking-tighter">
          {top_idea.theme.upper()} <span className="text-cyan-400">CORE</span>
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mb-12 leading-relaxed">
          {top_idea.summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-16">
          {{ {json.dumps(spec.get('features', []))}.map((f, i) => (
            <div key={{i}} className="bg-slate-900/50 p-6 rounded-xl border border-slate-800 hover:border-cyan-500/50 transition-all duration-300 group">
              <div className="w-8 h-8 rounded bg-slate-800 flex items-center justify-center mb-4 text-cyan-400 group-hover:bg-cyan-500/10 transition-colors">
                <span className="font-mono text-xs">0{{i + 1}}</span>
              </div>
              <h3 className="font-bold text-white text-lg mb-2 text-left tracking-tight">{{f}}</h3>
              <p className="text-slate-500 text-sm text-left leading-snug">Neural-link optimization for automated {top_idea.theme.lower()} processing.</p>
            </div>
          )) }}
        </div>

        <div className="relative group w-full max-w-2xl">
          <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-violet-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
          <div className="relative bg-slate-900 border border-slate-800 rounded-2xl p-10 flex flex-col items-center">
            <h2 className="text-3xl font-bold text-white mb-4 tracking-tight">Initiate Integration</h2>
            <p className="text-slate-400 mb-8 max-w-md">The organism is ready to deploy. Connect your node to the {top_idea.theme} network.</p>
            <div className="flex w-full max-w-md gap-3">
              <input type="email" placeholder="ACCESS_ID@PROTOCOL.NETWORK" className="flex-1 bg-slate-950 border border-slate-800 px-4 py-3 rounded-lg text-white text-sm font-mono focus:outline-none focus:border-cyan-500 transition-colors" />
              <button className="px-8 py-3 bg-cyan-500 text-slate-950 font-bold rounded-lg hover:bg-cyan-400 transition-colors uppercase text-xs tracking-tighter">
                Connect
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-24 text-slate-600 text-[10px] font-mono uppercase tracking-[0.2em] pb-12">
        &copy; {{new Date().getFullYear()}} {top_idea.theme} // ORGANISM-001 // SYSTEM-STATUS: OPTIMAL
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
