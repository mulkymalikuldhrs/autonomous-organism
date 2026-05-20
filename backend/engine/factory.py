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
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="{top_idea.theme} API")

@app.get("/api/features")
def get_features():
    return {json.dumps(spec.get('features', []))}

@app.get("/health")
def health():
    return {{"status": "healthy"}}

# Serve static files from frontend build
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
else:
    @app.get("/")
    def read_root():
        return {{"status": "online", "name": "{top_idea.theme}", "info": "Frontend not built yet"}}
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
      <nav className="w-full max-w-4xl flex justify-between items-center mb-12 py-4 border-b border-slate-800">
        <div className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-500 tracking-tighter">
          {top_idea.theme.upper()}
        </div>
        <div className="flex gap-6 text-xs font-bold uppercase tracking-widest text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Neural Grid</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Protocol</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Terminal</a>
        </div>
      </nav>

      <main className="w-full max-w-4xl flex flex-col items-center text-center">
        <div className="inline-block px-3 py-1 mb-6 rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-400 text-[10px] font-bold uppercase tracking-widest animate-pulse">
          Autonomous Solution Online
        </div>

        <h1 className="text-5xl md:text-7xl font-black text-white mb-6 leading-tight tracking-tighter">
          Evolutionary <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-500">{top_idea.theme}</span>
        </h1>

        <p className="text-slate-400 text-lg max-w-2xl mb-12 leading-relaxed">
          {top_idea.summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {{ {json.dumps(spec.get('features', []))}.map((f, i) => (
            <div key={{i}} className="group bg-slate-900/50 p-8 rounded-3xl border border-slate-800 hover:border-cyan-500/50 hover:bg-slate-900 transition-all duration-300 text-left relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1 h-0 bg-cyan-500 group-hover:h-full transition-all duration-300" />
              <div className="text-cyan-500 font-mono text-xs mb-4">NODE_0{{i + 1}}</div>
              <h3 className="font-bold text-white text-xl mb-3 tracking-tight group-hover:text-cyan-400 transition-colors">{{f}}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">Processing automated sub-routines to optimize human problem resolution within the digital ecosystem.</p>
            </div>
          )) }}
        </div>

        <div className="bg-gradient-to-br from-slate-900 to-slate-950 rounded-[40px] p-12 w-full border border-slate-800 flex flex-col items-center relative overflow-hidden">
          <div className="absolute -top-24 -right-24 w-48 h-48 bg-cyan-500/10 blur-[100px] rounded-full" />
          <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-violet-500/10 blur-[100px] rounded-full" />

          <h2 className="text-3xl font-black text-white mb-4 tracking-tight">Initiate Synchronization</h2>
          <p className="text-slate-400 mb-8 max-w-md">Connect your neural profile to the {top_idea.theme} organism and receive real-time evolution updates.</p>

          <div className="flex w-full max-w-md gap-3 bg-slate-950 p-2 rounded-2xl border border-slate-800">
            <input type="email" placeholder="neural@address.io" className="flex-1 bg-transparent px-4 py-3 text-white focus:outline-none text-sm" />
            <button className="px-8 py-3 bg-cyan-500 text-slate-950 font-black text-xs uppercase tracking-widest rounded-xl hover:bg-cyan-400 transition-all shadow-[0_0_20px_rgba(6,182,212,0.3)]">
              Sync Now
            </button>
          </div>
        </div>
      </main>

      <footer className="mt-24 text-slate-600 text-[10px] font-bold uppercase tracking-[0.2em] pb-12">
        [ SYSTEM_TYPE: OTONOM ] • &copy; {{new Date().getFullYear()}} {top_idea.theme} • GEN-4.1
      </footer>
    </div>
  );
}}
export default App;
""")

    # C. Dockerfile (Multi-stage)
    with open(f"{product_dir}/Dockerfile", "w") as f:
        f.write(f"""# Stage 1: Build Frontend
FROM node:20-slim AS build-frontend
WORKDIR /frontend
COPY frontend/package.json ./
# Mock package.json if it doesn't exist for build
RUN echo '{{"name": "frontend", "type": "module", "dependencies": {{"react": "^18.3.1", "react-dom": "^18.3.1", "lucide-react": "^0.462.0"}}, "devDependencies": {{"vite": "^5.4.19", "@vitejs/plugin-react": "^4.3.4"}}}}' > package.json
# In a real scenario, we would run npm install and npm run build
# For this autonomous MVP, we'll assume the frontend is a simple HTML/JS or pre-built
RUN mkdir -p dist && echo "<html><head><title>{top_idea.theme}</title></head><body><div id='root'></div><script>document.getElementById('root').innerHTML = '<h1>{top_idea.theme}</h1><p>{top_idea.summary}</p>';</script></body></html>" > dist/index.html

# Stage 2: Run Backend
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
COPY --from=build-frontend /frontend/dist ./static
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
