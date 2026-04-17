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
    prompt = f"""Generate a comprehensive technical blueprint for a SaaS MVP:
Idea: {top_idea.theme}
Summary: {top_idea.summary}

Output JSON with keys:
'db_schema': [list of SQL tables and columns]
'endpoints': [list of FastAPI endpoints with methods]
'features': [list of key features]
'ui_ux_strategy': [description of UI/UX]
'monetization_plan': [how it makes money]
'stack': {{'backend': 'FastAPI', 'frontend': 'React/Vite/Tailwind', 'db': 'SQLite'}}
"""
    spec_raw = await llm.generate(prompt, system="You are the SaaS Architect. Design modern, scalable solutions.")

    try:
        json_match = re.search(r"(\{.*\})", spec_raw, re.S)
        spec = json.loads(json_match.group(1)) if json_match else {"raw": spec_raw}
    except:
        spec = {"raw": spec_raw}

    os.makedirs("products", exist_ok=True)
    product_name = top_idea.theme.lower().replace(" ", "_").replace("/", "_").replace(":", "")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    product_dir = f"products/{product_name}_{timestamp}"
    os.makedirs(product_dir, exist_ok=True)

    # 2. Generate Files
    # A. backend/main.py
    backend_dir = f"{product_dir}/backend"
    os.makedirs(backend_dir, exist_ok=True)
    with open(f"{backend_dir}/main.py", "w") as f:
        f.write(f'''from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="{top_idea.theme} API")

@app.get("/")
def read_root():
    return {{"status": "online", "name": "{top_idea.theme}", "generation": 4}}

@app.get("/api/blueprint")
def get_blueprint():
    return {json.dumps(spec)}

@app.get("/health")
def health():
    return {{"status": "healthy"}}
''')

    # B. frontend/ (React Skeleton with Bioluminescent Tailwind Design)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)

    features_json = json.dumps(spec.get('features', []))

    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write('''
import React from 'react';

function App() {
  const features = ''' + features_json + ''';
  const theme = "''' + top_idea.theme + '''";
  const summary = "''' + top_idea.summary.replace('"', '\\"') + '''";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-8 font-sans selection:bg-cyan-500/30">
      {/* Bioluminescent background glow */}
      <div className="fixed top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-cyan-500/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-violet-600/10 rounded-full blur-[120px]" />
      </div>

      <nav className="w-full max-w-5xl flex justify-between items-center mb-20 backdrop-blur-md bg-slate-900/50 p-6 rounded-2xl border border-slate-800">
        <div className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">
          {theme}
        </div>
        <div className="flex gap-8 text-sm font-semibold tracking-wide uppercase text-slate-400">
          <a href="#" className="hover:text-cyan-400 transition-colors">Features</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Vision</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Terminal</a>
        </div>
      </nav>

      <main className="w-full max-w-4xl flex flex-col items-center text-center">
        <div className="inline-block px-4 py-1.5 mb-6 rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-400 text-xs font-bold tracking-widest uppercase">
          Autonomous Gen-4 Solution
        </div>

        <h1 className="text-6xl md:text-7xl font-black text-white mb-8 leading-tight tracking-tighter">
          Evolving <span className="bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">{theme}</span>
        </h1>

        <p className="text-slate-400 text-xl max-w-2xl mb-12 leading-relaxed">
          {summary}
        </p>

        <div className="flex gap-4 mb-20">
          <button className="px-8 py-4 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black rounded-xl transition-all hover:scale-105 hover:shadow-[0_0_20px_rgba(6,182,212,0.5)]">
            Deploy Now
          </button>
          <button className="px-8 py-4 bg-slate-900 border border-slate-800 hover:border-slate-700 text-white font-black rounded-xl transition-all">
            Documentation
          </button>
        </div>

        <div className="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-24">
          {features.map((f, i) => (
            <div key={i} className="group bg-slate-900/40 p-8 rounded-3xl border border-slate-800 hover:border-cyan-500/50 transition-all duration-300 backdrop-blur-sm">
              <div className="w-12 h-12 bg-slate-800 text-cyan-400 rounded-2xl flex items-center justify-center mb-6 font-black text-xl group-hover:bg-cyan-500 group-hover:text-slate-950 transition-colors">
                0{i + 1}
              </div>
              <h3 className="font-bold text-white text-xl mb-3 text-left tracking-tight">{f}</h3>
              <p className="text-slate-500 text-sm text-left leading-relaxed">Generated by SaaS Factory Gen-4. Automatically optimized for conversion and performance.</p>
            </div>
          ))}
        </div>

        <div className="relative bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-[40px] p-16 w-full overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-violet-600/20 rounded-full blur-[80px] -mr-32 -mt-32" />
          <h2 className="text-4xl font-black text-white mb-6 relative z-10">Access the Organism</h2>
          <p className="text-slate-400 mb-10 max-w-md mx-auto relative z-10 font-medium">Be the first to interface with the autonomous {theme} network.</p>
          <div className="flex w-full max-w-md mx-auto gap-3 relative z-10">
            <input type="email" placeholder="terminal@access.io" className="flex-1 bg-slate-950/50 border border-slate-700 px-6 py-4 rounded-2xl text-white focus:outline-none focus:border-cyan-500/50 transition-colors" />
            <button className="px-8 py-4 bg-white text-slate-950 font-black rounded-2xl hover:bg-cyan-400 transition-all">
              Join
            </button>
          </div>
        </div>
      </main>

      <footer className="mt-32 text-slate-600 text-sm pb-12 font-medium tracking-wide uppercase">
        &copy; {new Date().getFullYear()} {theme} &bull; Autonomous SaaS Organism Gen-4
      </footer>
    </div>
  );
}
export default App;
''')

    # C. Dockerfile
    with open(f"{product_dir}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
""")

    # D. requirements.txt
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

    db.add(models.EngineLog(level="success", source="Factory", message=f"Autonomous SaaS generated: {top_idea.theme} (Bioluminescent Edition)"))
    db.commit()
    return {"product": top_idea.theme, "path": product_dir}
