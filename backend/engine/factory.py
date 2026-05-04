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
'ui_ux_strategy': [description of layout and user flow]
'monetization_model': [how this product will make money]
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
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,_rgba(17,24,39,1)_0%,_rgba(2,6,23,1)_100%)] -z-10" />

      <nav className="w-full max-w-6xl flex justify-between items-center mb-20 backdrop-blur-sm bg-slate-900/40 p-6 rounded-2xl border border-slate-800/50">
        <div className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent tracking-tighter">
          {top_idea.theme.upper()}
        </div>
        <div className="flex gap-8 text-sm font-semibold text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Features</a>
          <a href="#" className="hover:text-violet-400 transition-colors">Pricing</a>
          <a href="#" className="px-5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-100 rounded-full transition-all border border-slate-700">Launch App</a>
        </div>
      </nav>

      <main className="w-full max-w-6xl flex flex-col items-center text-center">
        <div className="inline-block px-4 py-1.5 mb-6 text-xs font-bold tracking-widest text-cyan-400 uppercase bg-cyan-400/10 border border-cyan-400/20 rounded-full animate-pulse">
          Autonomous Gen-4 Solution
        </div>

        <h1 className="text-6xl md:text-8xl font-black text-white mb-8 leading-tight tracking-tight">
          Evolutionary <span className="bg-gradient-to-b from-cyan-300 to-cyan-500 bg-clip-text text-transparent">{top_idea.theme}</span>
        </h1>

        <p className="text-slate-400 text-xl max-w-3xl mb-16 leading-relaxed font-light">
          {top_idea.summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-8 mb-24">
          {{ {json.dumps(spec.get('features', []))}.map((f, i) => (
            <div key={{i}} className="group bg-slate-900/50 p-8 rounded-3xl border border-slate-800 hover:border-cyan-500/50 transition-all duration-500 hover:shadow-[0_0_30px_-10px_rgba(34,211,238,0.2)]">
              <div className="w-12 h-12 bg-gradient-to-br from-cyan-500/20 to-violet-500/20 text-cyan-400 rounded-2xl flex items-center justify-center mb-6 font-black text-xl border border-cyan-500/10 group-hover:scale-110 transition-transform">
                {{i + 1}}
              </div>
              <h3 className="font-bold text-white text-xl mb-3 text-left group-hover:text-cyan-400 transition-colors">{{f}}</h3>
              <p className="text-slate-500 text-sm text-left leading-relaxed">Generated autonomous logic ensuring high-performance execution of the {top_idea.theme} protocol.</p>
            </div>
          )) }}
        </div>

        <div className="relative bg-gradient-to-br from-slate-900 to-slate-950 text-white rounded-[3rem] p-16 w-full flex flex-col items-center border border-slate-800 overflow-hidden shadow-2xl">
          <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 blur-[100px] -z-10" />
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-violet-500/10 blur-[100px] -z-10" />

          <h2 className="text-4xl font-black mb-6 tracking-tight">Join the Digital Species</h2>
          <p className="text-slate-400 mb-10 max-w-lg text-lg">Experience the first autonomous SaaS built by the Gen-4 Organism. No legacy code, just evolution.</p>

          <div className="flex w-full max-w-md gap-3 p-2 bg-slate-800/50 rounded-2xl border border-slate-700/50 focus-within:border-cyan-500/50 transition-colors">
            <input type="email" placeholder="access_key@evolution.io" className="flex-1 px-4 py-3 bg-transparent text-white focus:outline-none placeholder:text-slate-600" />
            <button className="px-8 py-3 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black rounded-xl transition-all active:scale-95 shadow-lg shadow-cyan-500/20">
              GET ACCESS
            </button>
          </div>
        </div>

        <section className="w-full max-w-4xl mb-24 text-left border-l-2 border-violet-500/30 pl-8">
           <h3 className="text-violet-400 font-mono text-sm tracking-widest uppercase mb-4">Strategic Roadmap</h3>
           <div className="space-y-8">
              <div>
                <h4 className="text-white font-bold text-lg mb-2">UI/UX Strategy</h4>
                <p className="text-slate-500 text-sm leading-relaxed">{{ {json.dumps(spec.get('ui_ux_strategy', 'Autonomous interface design optimized for rapid problem resolution.'))} }}</p>
              </div>
              <div>
                <h4 className="text-white font-bold text-lg mb-2">Monetization Model</h4>
                <p className="text-slate-500 text-sm leading-relaxed">{{ {json.dumps(spec.get('monetization_model', 'Strategic revenue generation through autonomous value delivery.'))} }}</p>
              </div>
           </div>
        </section>
      </main>

      <footer className="mt-32 text-slate-600 text-xs pb-12 font-mono tracking-widest uppercase">
        &copy; {{new Date().getFullYear()}} {top_idea.theme} // ORGANISM GEN-4.1 // BIOLUMINESCENT EDITION
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
