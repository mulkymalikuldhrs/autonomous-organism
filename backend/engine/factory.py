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

    # 1. Brainstorming Complete Spec (Gen-4.1 Enhanced)
    prompt = f"""Generate a full technical specification for a SaaS MVP:
Idea: {top_idea.theme}
Summary: {top_idea.summary}

Output JSON with keys:
'db_schema': [list of SQL tables and columns]
'endpoints': [list of FastAPI endpoints with methods]
'features': [list of key features]
'ui_ux_strategy': "Detailed UI/UX strategy for bioluminescent theme"
'monetization_model': "Specific monetization model and pricing"
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
    # Using format() instead of f-string to avoid complex escaping of JSX curly braces
    app_jsx_template = """
import React from 'react';

function App() {{
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-8 font-sans selection:bg-cyan-500/30">
      {{/* Bioluminescent Background Elements */}}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-cyan-500/10 blur-[120px] rounded-full animate-pulse" />
        <div className="absolute top-[20%] -right-[5%] w-[30%] h-[30%] bg-violet-600/10 blur-[100px] rounded-full animate-pulse delay-700" />
      </div>

      <nav className="w-full max-w-5xl flex justify-between items-center mb-20 relative z-10 backdrop-blur-md bg-slate-900/50 p-4 rounded-2xl border border-slate-800">
        <div className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-400 tracking-tighter uppercase">{theme}</div>
        <div className="flex gap-8 text-xs font-bold uppercase tracking-widest text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Neural Features</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Core Nodes</a>
          <a href="#" className="px-4 py-2 bg-slate-800 text-cyan-400 rounded-lg border border-cyan-500/20 hover:bg-cyan-500/10 transition-all">Pulse Access</a>
        </div>
      </nav>

      <main className="w-full max-w-5xl flex flex-col items-center text-center relative z-10">
        <div className="inline-block px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-[10px] font-bold uppercase tracking-[0.2em] mb-6">
          Gen-4.1 Autonomous Evolution
        </div>

        <h1 className="text-6xl md:text-8xl font-black text-white mb-8 leading-[0.9] tracking-tighter">
          RECODING <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-500 italic">{theme_upper}</span>
        </h1>

        <p className="text-slate-400 text-lg max-w-2xl mb-12 leading-relaxed font-medium">
          {summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-4 mb-24">
          {{ {features_json}.map((f, i) => (
            <div key={{i}} className="group bg-slate-900/40 p-8 rounded-3xl border border-slate-800 hover:border-cyan-500/50 transition-all duration-500 text-left relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-100 transition-opacity">
                <div className="w-2 h-2 rounded-full bg-cyan-500 animate-ping" />
              </div>
              <div className="text-cyan-500/30 font-mono text-xs mb-4 group-hover:text-cyan-400 transition-colors">NODE_0{{i + 1}}</div>
              <h3 className="font-bold text-white text-xl mb-3 group-hover:translate-x-1 transition-transform">{{f}}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">Synthesizing autonomous protocols to solve human complexity at zero latency.</p>
            </div>
          )) }}
        </div>

        <div className="relative w-full max-w-4xl">
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-violet-600 blur-[80px] opacity-20" />
          <div className="relative bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-[40px] p-12 w-full flex flex-col items-center overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-cyan-500 via-transparent to-violet-600" />
            <h2 className="text-4xl font-bold text-white mb-4">Initiate Organism Sync</h2>
            <p className="text-slate-400 mb-10 max-w-md font-medium text-sm">Synchronize your workflow with the first {theme} autonomous agent fleet.</p>
            <div className="flex w-full max-w-md gap-3 bg-slate-950/50 p-2 rounded-2xl border border-slate-800">
              <input type="email" placeholder="neural_id@network.com" className="flex-1 bg-transparent px-4 py-3 rounded-xl text-white focus:outline-none font-mono text-sm" />
              <button className="px-8 py-3 bg-gradient-to-r from-cyan-500 to-cyan-600 text-slate-950 font-black rounded-xl hover:shadow-[0_0_20px_rgba(6,182,212,0.5)] transition-all uppercase text-xs tracking-tighter">
                Connect
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-32 text-slate-600 text-[10px] font-bold uppercase tracking-[0.3em] pb-12 relative z-10">
        &copy; {{new Date().getFullYear()}} {theme} // BIOLUMINESCENT EDITION // GEN-4.1
      </footer>
    </div>
  );
}}
export default App;
"""
    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write(app_jsx_template.format(
            theme=top_idea.theme,
            theme_upper=top_idea.theme.upper(),
            summary=top_idea.summary,
            features_json=json.dumps(spec.get('features', []))
        ))

    # C. Dockerfile
    with open(f"{product_dir}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
""")

    # D. docker-compose.yml (Port 8081 to avoid conflict with main organism)
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
