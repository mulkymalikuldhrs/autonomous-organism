from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import json
import re

async def run_factory(db: Session):
    log = models.EngineLog(level="info", source="Factory", message="SaaS Factory started (Gen-4 High-Quality Build)")
    db.add(log)
    db.commit()

    # Get top unprocessed idea
    top_idea = db.query(models.IdeaCandidate).filter(models.IdeaCandidate.is_processed == False).order_by(models.IdeaCandidate.score.desc()).first()
    if not top_idea:
        db.add(models.EngineLog(level="info", source="Factory", message="No new ideas to build."))
        db.commit()
        return

    # 1. Brainstorming Complete Spec
    prompt = f"""Generate a comprehensive technical specification for a SaaS MVP:
Idea: {top_idea.theme}
Summary: {top_idea.summary}

Output JSON with keys:
'db_schema': [list of SQL tables and columns with types]
'endpoints': [list of FastAPI endpoints with methods, description, and request/response models]
'features': [list of key features with detailed descriptions]
'ui_components': [list of necessary React components]
'stack': {{'backend': 'FastAPI', 'frontend': 'React/Vite/Tailwind', 'db': 'SQLite'}}
"""
    spec_raw = await llm.generate(prompt, system="You are the Lead SaaS Architect. Design systems that are scalable and maintainable.")

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

    features_json = json.dumps(spec.get('features', []))

    with open(f"{backend_dir}/main.py", "w") as f:
        f.write(f"""from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json

app = FastAPI(
    title="{top_idea.theme} API",
    description="{top_idea.summary}",
    version="0.1.0"
)

class Feature(BaseModel):
    name: str
    description: str

@app.get("/")
def read_root():
    return {{
        "status": "online",
        "name": "{top_idea.theme}",
        "message": "Welcome to the {top_idea.theme} API"
    }}

@app.get("/api/features", response_model=List[Feature])
def get_features():
    features = {features_json}
    if not features:
        return []
    if isinstance(features[0], str):
        return [{{'name': f, 'description': 'Automated feature description.'}} for f in features]
    return features

@app.get("/health")
def health():
    return {{"status": "healthy", "timestamp": "{datetime.datetime.now().isoformat()}"}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
""")

    # B. frontend/ (React Skeleton with Bioluminescent Tailwind Theme)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)

    react_code = """
import React, { useState, useEffect } from 'react';

function App() {
  const [features, setFeatures] = useState([]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-8 font-sans selection:bg-cyan-500/30">
      {/* Bioluminescent Glows */}
      <div className="fixed top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-cyan-500/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-violet-600/10 rounded-full blur-[120px]"></div>
      </div>

      <nav className="w-full max-w-5xl flex justify-between items-center mb-20 py-6 border-b border-slate-800/50">
        <div className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent tracking-tighter">
          """ + top_idea.theme.upper() + """
        </div>
        <div className="hidden md:flex gap-8 text-sm font-medium text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Features</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Solutions</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Pricing</a>
        </div>
        <button className="px-5 py-2 bg-slate-100 text-slate-950 rounded-full text-sm font-bold hover:bg-cyan-400 transition-all duration-300 shadow-[0_0_20px_rgba(255,255,255,0.1)]">
          Get Started
        </button>
      </nav>

      <main className="w-full max-w-5xl flex flex-col items-center text-center">
        <div className="inline-block px-4 py-1.5 mb-6 border border-cyan-500/30 bg-cyan-500/5 rounded-full text-xs font-bold text-cyan-400 uppercase tracking-widest">
          Autonomous Generation v4
        </div>
        <h1 className="text-6xl md:text-7xl font-black text-white mb-8 leading-[1.1] tracking-tight">
          Evolutionary <span className="bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent">SaaS Solutions</span>
        </h1>
        <p className="text-slate-400 text-xl max-w-3xl mb-12 leading-relaxed font-light">
          """ + top_idea.summary + """
        </p>

        <div className="flex gap-4 mb-24">
          <button className="px-8 py-4 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-2xl transition-all shadow-[0_0_30px_rgba(6,182,212,0.3)]">
            Launch Instance
          </button>
          <button className="px-8 py-4 bg-slate-900 border border-slate-800 hover:border-slate-700 text-white font-bold rounded-2xl transition-all">
            View Blueprint
          </button>
        </div>

        <div className="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-24">
          { """ + features_json + """.map((f, i) => (
            <div key={i} className="group bg-slate-900/40 backdrop-blur-xl p-8 rounded-3xl border border-slate-800/50 hover:border-cyan-500/50 transition-all duration-500 text-left">
              <div className="w-12 h-12 bg-gradient-to-br from-cyan-500/20 to-violet-500/20 text-cyan-400 rounded-2xl flex items-center justify-center mb-6 border border-cyan-500/20 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
              </div>
              <h3 className="font-bold text-white text-xl mb-3">{typeof f === 'string' ? f : f.name}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">{typeof f === 'string' ? 'Autonomous solution module deployed via Gen-4 factory pipeline.' : f.description}</p>
            </div>
          )) }
        </div>

        <div className="relative w-full bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-[3rem] p-16 overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full blur-[80px]"></div>
          <h2 className="text-4xl font-bold text-white mb-6">Join the Digital Species</h2>
          <p className="text-slate-400 mb-10 max-w-md mx-auto">Scale your operations with """ + top_idea.theme + """. Automated, decentralized, and otonom.</p>
          <div className="flex w-full max-w-md mx-auto gap-3 bg-slate-800/50 p-2 rounded-2xl border border-slate-700/50">
            <input type="email" placeholder="neural-link@example.com" className="flex-1 bg-transparent px-4 py-3 text-white focus:outline-none placeholder:text-slate-600" />
            <button className="px-6 py-3 bg-cyan-500 text-slate-950 font-bold rounded-xl hover:bg-cyan-400 transition-all shadow-lg shadow-cyan-500/20">
              Join
            </button>
          </div>
        </div>
      </main>

      <footer className="mt-32 text-slate-500 text-xs pb-12 w-full max-w-5xl flex justify-between border-t border-slate-900 pt-8">
        <div>&copy; {new Date().getFullYear()} """ + top_idea.theme.upper() + """</div>
        <div className="flex gap-6">
          <a href="#" className="hover:text-cyan-400">BLUEPRINT</a>
          <a href="#" className="hover:text-cyan-400">GENESIS</a>
          <a href="#" className="hover:text-cyan-400">TERMINATE</a>
        </div>
      </footer>
    </div>
  );
}
export default App;
"""
    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write(react_code)

    # C. Dockerfile
    with open(f"{product_dir}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
EXPOSE 8000
CMD ["python", "main.py"]
""")

    # D. docker-compose.yml
    with open(f"{product_dir}/docker-compose.yml", "w") as f:
        f.write(f"""version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - APP_NAME={top_idea.theme}
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
