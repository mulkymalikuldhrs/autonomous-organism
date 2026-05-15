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
'ui_ux_strategy': 'detailed description of bioluminescent design and user flow'
'monetization_model': 'detailed plan for revenue generation'
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

    # B. frontend/ (React Skeleton with Bioluminescent Design)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)
    with open(f"{frontend_dir}/api.js", "w") as f:
        f.write("""
export const apiClient = {
  async getFeatures() {
    const res = await fetch('/api/features');
    return res.json();
  },
  async checkHealth() {
    const res = await fetch('/health');
    return res.json();
  }
};
""")

    features_json = json.dumps(spec.get('features', []))
    app_jsx_template = """
import React, { useState, useEffect } from 'react';
import { apiClient } from './api';

function App() {
  const [features, setFeatures] = useState([]);

  useEffect(() => {
    apiClient.getFeatures().then(setFeatures).catch(console.error);
  }, []);

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 flex flex-col items-center p-8 font-sans selection:bg-cyan-500/30 overflow-x-hidden">
      {/* Background Glows */}
      <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-cyan-500/10 blur-[120px] rounded-full pointer-events-none" />
      <div className="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-violet-500/10 blur-[120px] rounded-full pointer-events-none" />

      <nav className="w-full max-w-5xl flex justify-between items-center mb-16 py-6 border-b border-slate-800/50 backdrop-blur-md sticky top-0 z-50">
        <div className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-sky-400 to-violet-500 tracking-tighter">
          __THEME__
        </div>
        <div className="flex gap-8 text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">
          <a href="#" className="hover:text-cyan-400 transition-all duration-300 hover:tracking-[0.3em]">Neural Grid</a>
          <a href="#" className="hover:text-cyan-400 transition-all duration-300 hover:tracking-[0.3em]">Protocol</a>
          <a href="#" className="hover:text-cyan-400 transition-all duration-300 hover:tracking-[0.3em]">Terminal</a>
        </div>
      </nav>

      <main className="w-full max-w-5xl flex flex-col items-center text-center relative z-10">
        <div className="inline-block px-4 py-1.5 mb-8 rounded-full border border-cyan-500/20 bg-cyan-500/5 text-cyan-400 text-[9px] font-bold uppercase tracking-[0.3em] animate-pulse shadow-[0_0_15px_rgba(6,182,212,0.1)]">
          Autonomous Solution Online // Node___TIMESTAMP__
        </div>

        <h1 className="text-6xl md:text-8xl font-black text-white mb-8 leading-[0.9] tracking-tighter">
          The Future of <br/>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-white to-violet-500 animate-gradient-x">
            __THEME__
          </span>
        </h1>

        <p className="text-slate-400 text-xl max-w-2xl mb-16 leading-relaxed font-light">
          __SUMMARY__
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-24">
          {(features.length > 0 ? features : __FEATURES__).map((f, i) => (
            <div key={i} className="group bg-slate-900/20 backdrop-blur-sm p-10 rounded-[2rem] border border-slate-800/50 hover:border-cyan-500/40 hover:bg-slate-900/40 transition-all duration-500 text-left relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="text-cyan-500/50 font-mono text-[10px] mb-6 tracking-widest uppercase">Sub-Routine 0x0{i + 1}</div>
              <h3 className="font-bold text-white text-2xl mb-4 tracking-tight group-hover:text-cyan-400 transition-colors duration-300">{f}</h3>
              <p className="text-slate-500 text-sm leading-relaxed group-hover:text-slate-400 transition-colors duration-300">
                Deploying autonomous intelligence to resolve complex human challenges within the digital manifold.
              </p>
            </div>
          ))}
        </div>

        <div className="bg-gradient-to-br from-slate-900/50 to-slate-950/50 backdrop-blur-xl rounded-[3rem] p-16 w-full border border-slate-800/50 flex flex-col items-center relative overflow-hidden shadow-2xl">
          <div className="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-5 pointer-events-none" />

          <h2 className="text-4xl font-black text-white mb-6 tracking-tight">Sync with the Organism</h2>
          <p className="text-slate-400 mb-10 max-w-md text-lg font-light">Connect your neural address to join the evolution of __THEME__.</p>

          <div className="flex w-full max-w-lg gap-4 bg-slate-950/80 p-3 rounded-[1.5rem] border border-slate-800/50 focus-within:border-cyan-500/50 transition-all duration-300">
            <input type="email" placeholder="neural@address.io" className="flex-1 bg-transparent px-6 py-4 text-white focus:outline-none text-sm placeholder:text-slate-700" />
            <button className="px-10 py-4 bg-white text-slate-950 font-black text-[10px] uppercase tracking-[0.2em] rounded-xl hover:bg-cyan-400 hover:text-white transition-all duration-300 shadow-[0_0_30px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(6,182,212,0.3)]">
              Initialize
            </button>
          </div>
        </div>
      </main>

      <footer className="mt-32 text-slate-700 text-[9px] font-bold uppercase tracking-[0.4em] pb-16 flex flex-col items-center gap-4">
        <div className="w-12 h-[1px] bg-slate-800" />
        <div>[ STATUS: EVOLVING ] • &copy; __YEAR__ __THEME__ • GEN-4.1 OTONOM</div>
      </footer>
    </div>
  );
}
export default App;
"""
    app_jsx_content = app_jsx_template.replace("__THEME__", top_idea.theme.upper()) \
                                       .replace("__TIMESTAMP__", timestamp) \
                                       .replace("__SUMMARY__", top_idea.summary) \
                                       .replace("__FEATURES__", features_json) \
                                       .replace("__YEAR__", str(datetime.datetime.now().year))

    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write(app_jsx_content)

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
        f.write("fastapi\nuvicorn\npydantic\nsqlalchemy\n")

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
