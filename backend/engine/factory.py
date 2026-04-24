from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import json
import re

async def run_factory(db: Session):
    log = models.EngineLog(level="info", source="Factory", message="SaaS Factory started (Gen-4 Bioluminescent Edition)")
    db.add(log)
    db.commit()

    # Get top unprocessed idea
    top_idea = db.query(models.IdeaCandidate).filter(models.IdeaCandidate.is_processed == False).order_by(models.IdeaCandidate.score.desc()).first()
    if not top_idea:
        db.add(models.EngineLog(level="info", source="Factory", message="No new ideas to build."))
        db.commit()
        return

    # 1. Brainstorming Complete Spec
    prompt = f"""Generate a full technical blueprint for a SaaS MVP:
Idea: {top_idea.theme}
Summary: {top_idea.summary}

Output JSON with keys:
'db_schema': [{{'table': 'name', 'columns': ['col1 type', 'col2 type']}}]
'endpoints': [{{'path': '/api/path', 'method': 'GET/POST', 'description': 'desc'}}]
'features': [list of key features]
'ui_strategy': 'description of bioluminescent design implementation'
'monetization_plan': 'how to make money'
"""
    spec_raw = await llm.generate(prompt, system="You are the SaaS Architect. Design for high scale and autonomy.")

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
    return {{"status": "online", "name": "{top_idea.theme}", "version": "1.0.0-bioluminescent"}}

@app.get("/api/features")
def get_features():
    return {json.dumps(spec.get('features', []))}

@app.get("/api/blueprint")
def get_blueprint():
    return {json.dumps(spec)}

@app.get("/health")
def health():
    return {{"status": "healthy"}}
""")

    # B. frontend/ (React Skeleton with Bioluminescent Design)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)
    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write(f"""
import React from 'react';

function App() {{
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-8 font-sans selection:bg-cyan-500/30">
      <nav className="w-full max-w-5xl flex justify-between items-center mb-16 border-b border-slate-800 pb-6">
        <div className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent tracking-tighter">
          {top_idea.theme.upper()}
        </div>
        <div className="flex gap-8 text-sm font-medium text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Vision</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Tech Stack</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Pricing</a>
        </div>
      </nav>

      <main className="w-full max-w-5xl flex flex-col items-center">
        <div className="relative group mb-12">
          <div className="absolute -inset-1 bg-gradient-to-r from-cyan-600 to-violet-600 rounded-lg blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
          <h1 className="relative text-6xl md:text-7xl font-black text-white mb-6 leading-tight text-center tracking-tight">
            The Future of <span className="text-cyan-400">{top_idea.theme}</span>
          </h1>
        </div>

        <p className="text-slate-400 text-xl max-w-3xl mb-16 leading-relaxed text-center">
          {top_idea.summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-24">
          {{ {json.dumps(spec.get('features', []))}.map((f, i) => (
            <div key={{i}} className="bg-slate-900/50 p-8 rounded-3xl border border-slate-800 hover:border-cyan-500/50 transition-all duration-300 group">
              <div className="w-12 h-12 bg-slate-800 text-cyan-400 rounded-xl flex items-center justify-center mb-6 font-bold text-xl group-hover:bg-cyan-500/10 transition-colors">
                {{i + 1}}
              </div>
              <h3 className="font-bold text-white text-xl mb-3">{{f}}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">Autonomous module engineered for the {top_idea.theme} ecosystem.</p>
            </div>
          )) }}
        </div>

        <div className="relative w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-[3rem] p-12 overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 blur-[100px] -mr-32 -mt-32"></div>
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-violet-500/10 blur-[100px] -ml-32 -mb-32"></div>

          <div className="relative flex flex-col items-center text-center">
            <h2 className="text-4xl font-bold text-white mb-4">Initialize Growth</h2>
            <p className="text-slate-400 mb-10 max-w-md text-lg">Secure your spot in the autonomous evolution of {top_idea.theme}.</p>
            <div className="flex w-full max-w-md gap-3 bg-slate-950 p-2 rounded-2xl border border-slate-800 focus-within:border-cyan-500/50 transition-colors">
              <input type="email" placeholder="neural-link@example.com" className="flex-1 bg-transparent px-4 py-3 text-white focus:outline-none placeholder:text-slate-600" />
              <button className="px-8 py-3 bg-cyan-500 text-slate-950 font-bold rounded-xl hover:bg-cyan-400 transition-colors shadow-[0_0_20px_rgba(6,182,212,0.3)]">
                Deploy
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-32 text-slate-600 text-sm pb-12 flex flex-col items-center gap-4">
        <div className="flex gap-6">
          <a href="#" className="hover:text-slate-400 transition-colors">Status</a>
          <a href="#" className="hover:text-slate-400 transition-colors">Protocol</a>
          <a href="#" className="hover:text-slate-400 transition-colors">Security</a>
        </div>
        <p>&copy; {{new Date().getFullYear()}} {top_idea.theme.upper()}. SECURED BY ORGANISME SAAS OTONOM.</p>
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

    db.add(models.EngineLog(level="success", source="Factory", message=f"Full Bioluminescent SaaS structure generated for: {top_idea.theme}"))
    db.commit()
    return {"product": top_idea.theme, "path": product_dir}
