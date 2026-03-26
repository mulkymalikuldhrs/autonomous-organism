from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import json
import re

async def run_factory(db: Session):
    log = models.EngineLog(level="info", source="Factory", message="SaaS Factory started (Gen-4 Complete Build)")
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

    # B. frontend/ (React Skeleton)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)
    with open(f"{frontend_dir}/App.jsx", "w") as f:
        f.write(f"""
import React from 'react';

function App() {{
  const features = {json.dumps(spec.get('features', []))};

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <nav className="p-6 flex justify-between items-center bg-white shadow-sm">
        <div className="text-2xl font-bold text-indigo-600">{top_idea.theme}</div>
        <button className="px-5 py-2 rounded-full bg-indigo-600 text-white font-medium hover:bg-indigo-700 transition">
          Get Started
        </button>
      </nav>

      <main className="max-w-5xl mx-auto px-6 py-16 md:py-24 text-center">
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-slate-900 mb-8 leading-tight">
          Solving <span className="text-indigo-600">{top_idea.theme}</span> for Everyone
        </h1>
        <p className="text-xl text-slate-600 max-w-2xl mx-auto mb-12 leading-relaxed">
          {top_idea.summary}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
          {{features.map((feature, idx) => (
            <div key={{idx}} className="p-8 bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition">
              <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mb-6 text-indigo-600 font-bold">
                {{idx + 1}}
              </div>
              <h3 className="text-xl font-bold mb-3">{{feature}}</h3>
              <p className="text-slate-500 leading-relaxed">
                Automated implementation of {{feature}} to streamline your autonomous workflow.
              </p>
            </div>
          ))}}
        </div>

        <div className="mt-20 p-12 bg-indigo-900 rounded-[3rem] text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to automate?</h2>
          <p className="text-indigo-200 mb-8 text-lg">Join the waitlist for the {top_idea.theme} autonomous beta.</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto">
            <input type="email" placeholder="Enter your email" className="px-6 py-4 rounded-full text-slate-900 focus:outline-none w-full" />
            <button className="px-8 py-4 rounded-full bg-indigo-500 text-white font-bold hover:bg-indigo-400 transition whitespace-nowrap">
              Join Waitlist
            </button>
          </div>
        </div>
      </main>

      <footer className="py-12 border-t border-slate-100 text-center text-slate-400 text-sm">
        &copy; {{new Date().getFullYear()}} {top_idea.theme} • Powered by Autonomous SaaS Organism
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
