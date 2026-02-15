from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import json

async def run_factory(db: Session):
    log = models.EngineLog(level="info", source="Factory", message="SaaS Factory started")
    db.add(log)
    db.commit()

    # Get top unprocessed idea
    top_idea = db.query(models.IdeaCandidate).filter(models.IdeaCandidate.is_processed == False).order_by(models.IdeaCandidate.score.desc()).first()
    if not top_idea:
        db.add(models.EngineLog(level="info", source="Factory", message="No new ideas to build."))
        db.commit()
        return

    # Generate structured blueprint using LLM
    prompt = f"""Generate a detailed technical blueprint for this SaaS idea:
Idea: {top_idea.theme}
Summary: {top_idea.summary}

The blueprint must include:
1. Database Schema (SQL)
2. API Endpoints (FastAPI)
3. Frontend Component structure (React + Tailwind)
4. Core Business Logic pseudo-code
5. Monetization strategy

Provide ONLY valid JSON with keys: 'database_schema', 'api_endpoints', 'frontend_structure', 'business_logic', 'monetization_plan'."""
    llm_output = await llm.generate(prompt, system="You are the SaaS Factory Agent.")

    try:
        # Try to extract JSON if LLM returned extra text
        import re
        json_match = re.search(r"(\{.*\})", llm_output, re.S)
        if json_match:
            details = json.loads(json_match.group(1))
        else:
            details = {"raw": llm_output}
    except:
        details = {"raw": llm_output}

    product_name = "".join(x for x in top_idea.theme.title() if x.isalnum())
    product_dir = f"products/{product_name.lower()}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(product_dir, exist_ok=True)

    # Generate actual files
    # 1. Blueprint JSON
    blueprint_path = f"{product_dir}/blueprint.json"
    blueprint = {
        "idea_id": top_idea.id,
        "theme": top_idea.theme,
        "summary": top_idea.summary,
        "technical_details": details,
        "generated_at": str(datetime.datetime.now())
    }
    with open(blueprint_path, "w") as f:
        json.dump(blueprint, f, indent=2)

    # 2. Basic Backend (FastAPI)
    backend_code_prompt = f"Generate a single file FastAPI application for this SaaS: {top_idea.theme}. Summary: {top_idea.summary}. Requirements: {json.dumps(details.get('api_endpoints', {}))}. Return ONLY the python code."
    backend_code = await llm.generate(backend_code_prompt, system="You are the SaaS Backend Engineer Agent.")
    with open(f"{product_dir}/main.py", "w") as f:
        f.write(backend_code)

    # 3. Basic Frontend (HTML/Tailwind)
    frontend_code_prompt = f"Generate a single file HTML/Tailwind/JS frontend for this SaaS: {top_idea.theme}. Summary: {top_idea.summary}. It should call the backend at /api. Return ONLY the HTML code."
    frontend_code = await llm.generate(frontend_code_prompt, system="You are the SaaS Frontend Engineer Agent.")
    with open(f"{product_dir}/index.html", "w") as f:
        f.write(frontend_code)

    # Create product record
    new_product = models.Product(
        idea_id=top_idea.id,
        name=top_idea.theme,
        blueprint_path=blueprint_path
    )
    db.add(new_product)

    # Mark idea as processed
    top_idea.is_processed = True

    db.add(models.EngineLog(level="info", source="Factory", message=f"Built product: {top_idea.theme}. Blueprint: {filepath}"))
    db.commit()
