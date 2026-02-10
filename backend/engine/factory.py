from sqlalchemy.orm import Session
from ..models import EngineLog, IdeaCandidate
from .llm import generate_text
import asyncio
import os
import json

async def run_factory(db: Session, run_id: int):
    log = EngineLog(run_id=run_id, level="info", source="FACTORY", message="SaaS Factory: Materializing solution from top idea...")
    db.add(log)
    db.commit()

    top_idea = db.query(IdeaCandidate).order_by(IdeaCandidate.score.desc()).first()
    if not top_idea:
        log = EngineLog(run_id=run_id, level="warning", source="FACTORY", message="No idea candidates found. Waiting for Decision Core.")
        db.add(log)
        db.commit()
        return False

    # Real action: Create a product directory and scaffold a basic README/structure
    product_slug = top_idea.theme.replace(" ", "_").replace("/", "_").lower()[:50]
    base_path = f"products/{product_slug}"
    os.makedirs(base_path, exist_ok=True)

    scaffold = {
        "name": top_idea.theme,
        "description": top_idea.summary,
        "features": ["AI Analysis", "Problem Tracking", "Automated Outreach"],
        "tech_stack": "FastAPI + React + SQLite"
    }

    with open(f"{base_path}/blueprint.json", "w") as f:
        json.dump(scaffold, f, indent=2)

    # Use LLM to generate a more detailed README
    llm_prompt = f"Create a technical README for a SaaS idea: {top_idea.theme}. Summary: {top_idea.summary}"
    detailed_readme = await generate_text(llm_prompt)

    with open(f"{base_path}/README.md", "w") as f:
        f.write(f"# {top_idea.theme}\n\n## LLM Generated Blueprint\n{detailed_readme}\n\n## Summary\n{top_idea.summary}\n\n## Generation Meta\n- Run ID: {run_id}\n- Score: {top_idea.score}")

    log = EngineLog(run_id=run_id, level="success", source="FACTORY", message=f"Product scaffolded in /{base_path}. Real files generated with LLM assistance.")
    db.add(log)
    db.commit()
    return True
