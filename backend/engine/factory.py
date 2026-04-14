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

    # B. frontend/ (React Skeleton with Bioluminescent Design)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)
    with open(f"{frontend_dir}/App.jsx", "w") as f:
        # Use simple string formatting to avoid brace escaping issues in triple quoted f-strings
        content = """
import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-4 md:p-8 font-sans selection:bg-cyan-500/30">
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(17,24,39,1),rgba(2,6,23,1))] -z-10" />
      <div className="fixed top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent shadow-[0_0_15px_rgba(6,182,212,0.5)]" />

      <nav className="w-full max-w-5xl flex justify-between items-center mb-16 backdrop-blur-md bg-slate-900/50 p-4 rounded-2xl border border-slate-800/50 sticky top-4 z-50">
        <div className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-500 tracking-tighter hover:scale-105 transition-transform cursor-pointer">
          """ + top_idea.theme + """
        </div>
        <div className="hidden md:flex gap-8 text-sm font-semibold text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Features</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Solutions</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Pricing</a>
        </div>
        <button className="px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-bold rounded-full shadow-[0_0_20px_rgba(8,145,178,0.3)] transition-all active:scale-95">
          Get Started
        </button>
      </nav>

      <main className="w-full max-w-5xl flex flex-col items-center text-center">
        <div className="inline-block px-4 py-1.5 mb-6 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-bold tracking-widest uppercase animate-pulse">
          Autonomous Solution Gen-4
        </div>

        <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-8 leading-[1.1] tracking-tight">
          Evolutionary <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">""" + top_idea.theme + """</span>
        </h1>

        <p className="text-slate-400 text-lg md:text-xl max-w-3xl mb-12 leading-relaxed">
          """ + top_idea.summary + """
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-6 mb-20">
          """ + "".join([f"""
            <div className="group bg-slate-900/40 p-8 rounded-3xl border border-slate-800/50 hover:border-cyan-500/50 hover:bg-slate-900/60 transition-all duration-300 relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-cyan-500 to-violet-500 opacity-0 group-hover:opacity-100 transition-opacity" />
              <div className="w-12 h-12 bg-cyan-500/10 text-cyan-400 rounded-2xl flex items-center justify-center mb-6 font-bold text-xl group-hover:scale-110 transition-transform">
                {i+1}
              </div>
              <h3 className="font-bold text-white text-xl mb-3 text-left">{feature}</h3>
              <p className="text-slate-500 text-sm text-left leading-relaxed">Intelligence-driven automation component designed to optimize your workflow with minimal overhead.</p>
            </div>
          """ for i, feature in enumerate(spec.get('features', []))]) + """
        </div>

        <div className="relative w-full max-w-4xl bg-gradient-to-br from-slate-900 to-slate-950 rounded-[3rem] p-1 md:p-12 border border-slate-800 overflow-hidden">
          <div className="absolute -top-24 -right-24 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl" />
          <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-violet-500/10 rounded-full blur-3xl" />

          <div className="relative z-10 flex flex-col items-center">
            <h2 className="text-4xl font-bold text-white mb-6 tracking-tight">Ready for the Next Generation?</h2>
            <p className="text-slate-400 mb-10 max-w-md text-lg">Join the autonomous revolution. Enter your email to get early access to """ + top_idea.theme + """.</p>

            <div className="flex flex-col sm:flex-row w-full max-w-lg gap-3">
              <input
                type="email"
                placeholder="you@domain.com"
                className="flex-1 px-6 py-4 rounded-2xl bg-slate-800 border border-slate-700 text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500 transition-colors"
              />
              <button className="px-8 py-4 bg-white text-slate-950 font-bold rounded-2xl hover:bg-cyan-400 hover:text-white transition-all active:scale-95 shadow-xl shadow-white/5">
                Join Beta
              </button>
            </div>
            <p className="mt-6 text-slate-500 text-xs">No spam. Only autonomous updates.</p>
          </div>
        </div>
      </main>

      <footer className="mt-24 text-slate-500 text-sm pb-12 w-full max-w-5xl border-t border-slate-900 pt-8 flex flex-col md:row justify-between items-center gap-4">
        <div>&copy; {new Date().getFullYear()} """ + top_idea.theme + """. All rights reserved.</div>
        <div className="flex gap-6">
          <a href="#" className="hover:text-slate-300">Privacy</a>
          <a href="#" className="hover:text-slate-300">Terms</a>
          <a href="#" className="hover:text-slate-300">Contact</a>
        </div>
      </footer>
    </div>
  );
}
export default App;
"""
        f.write(content)

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
