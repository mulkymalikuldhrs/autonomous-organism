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
    prompt = f"Generate a technical blueprint for this SaaS idea:\nIdea: {top_idea.theme}\nSummary: {top_idea.summary}\n\nProvide JSON with keys: 'schema', 'endpoints', 'frontend_components'."
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

    os.makedirs("products", exist_ok=True)
    product_name = top_idea.theme.lower().replace(" ", "_")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"products/{product_name}_{timestamp}.json"

    blueprint = {
        "idea_id": top_idea.id,
        "theme": top_idea.theme,
        "summary": top_idea.summary,
        "technical_details": details,
        "generated_at": str(datetime.datetime.now())
    }

    with open(filepath, "w") as f:
        json.dump(blueprint, f, indent=2)

    # Create product record
    new_product = models.Product(
        idea_id=top_idea.id,
        name=top_idea.theme,
        blueprint_path=filepath
    )
    db.add(new_product)

    # Mark idea as processed
    top_idea.is_processed = True

    db.add(models.EngineLog(level="info", source="Factory", message=f"Built product: {top_idea.theme}. Blueprint: {filepath}"))
    db.commit()
