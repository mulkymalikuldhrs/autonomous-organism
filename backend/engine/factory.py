from ..database import SessionLocal, Product, IdeaCandidate, LifeLog
from .llm import call_llm
import json
import os

def run_factory():
    db = SessionLocal()
    try:
        best_idea = db.query(IdeaCandidate).order_by(IdeaCandidate.score.desc()).first()
        if not best_idea:
            return

        product_name = "".join(x for x in best_idea.theme.title() if not x.isspace())
        if not product_name.endswith("App"): product_name += "App"

        project_dir = f"products/{product_name.lower()}"
        os.makedirs(project_dir, exist_ok=True)

        # Real code generation via LLM
        prompt = (
            f"Generate a functional FastAPI backend for a SaaS called '{product_name}'. "
            f"The goal is: {best_idea.summary}. "
            "Return ONLY the content of main.py. No markdown, no explanations."
        )
        backend_code = call_llm(prompt, system_prompt="You are a senior full-stack developer.")

        with open(f"{project_dir}/main.py", "w") as f:
            f.write(backend_code)

        with open(f"{project_dir}/README.md", "w") as f:
            f.write(f"# {product_name}\n\n{best_idea.summary}\n\n## Strategy\n{best_idea.technical_spec}")

        new_product = Product(
            name=product_name,
            theme=best_idea.theme,
            status="built",
            url=f"http://localhost:8001/{product_name.lower()}"
        )
        db.add(new_product)
        db.add(LifeLog(engine="factory", type="success", message=f"Autonomous Build Complete: {product_name}"))
        db.commit()
    finally:
        db.close()
