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

        # 1. Generate FastAPI Backend
        backend_prompt = (
            f"Generate a functional FastAPI backend for a SaaS called '{product_name}'. "
            f"The goal is: {best_idea.summary}. "
            "Return ONLY the content of main.py. No markdown, no explanations."
        )
        backend_code = call_llm(backend_prompt, system_prompt="You are a senior full-stack developer.")
        with open(f"{project_dir}/main.py", "w") as f:
            f.write(backend_code)

        # 2. Generate Dockerfile
        dockerfile_content = f"""FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        with open(f"{project_dir}/Dockerfile", "w") as f:
            f.write(dockerfile_content)

        # 3. Generate requirements.txt
        with open(f"{project_dir}/requirements.txt", "w") as f:
            f.write("fastapi\nuvicorn\npydantic\n")

        # 4. Generate docker-compose.yml
        docker_compose_content = f"""version: '3.8'
services:
  {product_name.lower()}:
    build: .
    ports:
      - "8001:8000"
    environment:
      - PRODUCT_NAME={product_name}
    restart: always
"""
        with open(f"{project_dir}/docker-compose.yml", "w") as f:
            f.write(docker_compose_content)

        with open(f"{project_dir}/README.md", "w") as f:
            f.write(f"# {product_name}\n\n{best_idea.summary}\n\n## Strategy\n{best_idea.technical_spec}")

        new_product = Product(
            name=product_name,
            theme=best_idea.theme,
            status="built",
            url=f"http://localhost:8001"
        )
        db.add(new_product)
        db.add(LifeLog(engine="factory", type="success", message=f"Autonomous Build Complete: {product_name} (with Docker artifacts)"))
        db.commit()
    finally:
        db.close()
