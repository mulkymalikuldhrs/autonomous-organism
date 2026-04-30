from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import json
import re

async def run_factory(db: Session):
    log = models.EngineLog(level="info", source="Factory", message="SaaS Factory started (Gen-4.1 Runnable Production-Ready)")
    db.add(log)
    db.commit()

    # Get top unprocessed idea
    top_idea = db.query(models.IdeaCandidate).filter(models.IdeaCandidate.is_processed == False).order_by(models.IdeaCandidate.score.desc()).first()
    if not top_idea:
        db.add(models.EngineLog(level="info", source="Factory", message="No new ideas to build."))
        db.commit()
        return

    # 1. Brainstorming Complete Spec
    prompt = f"""Generate a comprehensive technical specification and business strategy for a SaaS MVP:
Idea: {top_idea.theme}
Summary: {top_idea.summary}

Output JSON with keys:
'db_schema': [list of SQL tables and columns with data types]
'endpoints': [list of FastAPI endpoints with methods and request/response models]
'features': [list of key features]
'ui_ux_strategy': [description of the bioluminescent design system implementation]
'monetization_model': [detailed plan: e.g. Tiered Subscription, Affiliate, etc.]
'stack': {{'backend': 'FastAPI', 'frontend': 'React/Vite/Tailwind', 'db': 'SQLite'}}
"""
    spec_raw = await llm.generate(prompt, system="You are the Lead Architect of the Autonomous Organism.")

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
    return {{"status": "online", "name": "{top_idea.theme}", "generation": "4.1"}}

@app.get("/api/spec")
def get_spec():
    return {json.dumps(spec)}

@app.get("/health")
def health():
    return {{"status": "healthy"}}
""")

    # B. frontend/ (Bioluminescent Edition)
    frontend_dir = f"{product_dir}/frontend"
    os.makedirs(frontend_dir, exist_ok=True)
    with open(f"{frontend_dir}/index.html", "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{top_idea.theme}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""")

    src_dir = f"{frontend_dir}/src"
    os.makedirs(src_dir, exist_ok=True)

    with open(f"{src_dir}/main.jsx", "w") as f:
        f.write("""import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""")

    with open(f"{src_dir}/index.css", "w") as f:
        f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;")

    with open(f"{src_dir}/App.jsx", "w") as f:
        f.write(f"""
import React from 'react';

function App() {{
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-8 font-sans selection:bg-cyan-500 selection:text-white">
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(17,24,39,1),rgba(2,6,23,1))] -z-10" />

      <nav className="w-full max-w-5xl flex justify-between items-center mb-16 backdrop-blur-md bg-white/5 p-6 rounded-2xl border border-white/10 shadow-2xl shadow-cyan-500/5">
        <div className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent tracking-tighter uppercase">
          {top_idea.theme}
        </div>
        <div className="flex gap-8 text-sm font-bold tracking-widest uppercase">
          <a href="#" className="hover:text-cyan-400 transition-colors">Core</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Neural</a>
          <a href="#" className="hover:text-cyan-400 transition-colors">Access</a>
        </div>
      </nav>

      <main className="w-full max-w-5xl flex flex-col items-center text-center">
        <div className="inline-block px-4 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-[10px] font-black uppercase tracking-[0.2em] mb-8 animate-pulse">
          Autonomous Species v4.1
        </div>

        <h1 className="text-6xl md:text-8xl font-black text-white mb-8 tracking-tighter leading-none">
          Evolve your <span className="bg-gradient-to-r from-cyan-400 to-violet-600 bg-clip-text text-transparent">Workflow.</span>
        </h1>

        <p className="text-slate-400 text-xl max-w-3xl mb-12 leading-relaxed font-light">
          {top_idea.summary}
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          {{ {json.dumps(spec.get('features', []))}.slice(0, 3).map((f, i) => (
            <div key={{i}} className="group bg-white/5 p-8 rounded-3xl border border-white/10 hover:border-cyan-500/50 hover:bg-white/10 transition-all duration-500 text-left">
              <div className="w-12 h-12 bg-gradient-to-br from-cyan-500 to-violet-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-cyan-500/20 group-hover:scale-110 transition-transform">
                <div className="w-6 h-6 border-2 border-white/30 rounded-full" />
              </div>
              <h3 className="font-bold text-white text-xl mb-4 tracking-tight">{{f}}</h3>
              <p className="text-slate-500 text-sm leading-relaxed font-medium">Neural architecture designed for autonomous problem-solving and organic growth.</p>
            </div>
          )) }}
        </div>

        <div className="relative bg-gradient-to-br from-slate-900 to-slate-950 rounded-[3rem] p-16 w-full border border-white/5 overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 blur-[120px] -z-10 rounded-full" />
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-violet-600/10 blur-[120px] -z-10 rounded-full" />

          <h2 className="text-4xl font-black text-white mb-6 uppercase tracking-tighter">Initiate Integration</h2>
          <p className="text-slate-400 mb-10 max-w-lg mx-auto font-medium">Join the next generation of SaaS. Fully autonomous, fully decentralized, fully organic.</p>

          <div className="flex flex-col sm:flex-row w-full max-w-md mx-auto gap-4">
            <input type="email" placeholder="NEURAL_ID@SYSTEM.COM" className="flex-1 px-6 py-4 rounded-2xl bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cyan-500 transition-colors text-center font-bold tracking-widest text-xs uppercase" />
            <button className="px-10 py-4 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black rounded-2xl transition-all hover:scale-105 active:scale-95 shadow-xl shadow-cyan-500/20 uppercase text-xs tracking-widest">
              SYNC NOW
            </button>
          </div>
        </div>
      </main>

      <footer className="mt-32 text-slate-600 text-[10px] font-black uppercase tracking-[0.5em] pb-12">
        &copy; {{new Date().getFullYear()}} {top_idea.theme} // ORGANISME SAAS OTONOM // ALL SYSTEMS LIVE
      </footer>
    </div>
  );
}}
export default App;
""")

    # Configs
    with open(f"{frontend_dir}/package.json", "w") as f:
        f.write(json.dumps({
            "name": product_name,
            "private": True,
            "version": "0.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "devDependencies": {
                "@types/react": "^18.2.66",
                "@types/react-dom": "^18.2.22",
                "@vitejs/plugin-react": "^4.2.1",
                "autoprefixer": "^10.4.19",
                "postcss": "^8.4.38",
                "tailwindcss": "^3.4.3",
                "vite": "^5.2.0"
            }
        }, indent=2))

    with open(f"{frontend_dir}/tailwind.config.js", "w") as f:
        f.write("""/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
""")

    with open(f"{frontend_dir}/vite.config.js", "w") as f:
        f.write("""import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
})
""")

    with open(f"{frontend_dir}/postcss.config.js", "w") as f:
        f.write("export default { plugins: { tailwindcss: {}, autoprefixer: {}, }, }")

    # C. Dockerfile
    with open(f"{product_dir}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
EXPOSE 80
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

    db.add(models.EngineLog(level="success", source="Factory", message=f"Full Gen-4.1 Runnable SaaS generated: {top_idea.theme}"))
    db.commit()
    return {"product": top_idea.theme, "path": product_dir}
