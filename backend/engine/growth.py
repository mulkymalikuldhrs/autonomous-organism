from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import random

MARKETING_TEMPLATES = {
    "Twitter/X": "I'm launching a new tool that solves: {problem}. It's called {name}. 🚀 #SaaS #Growth",
    "Reddit": "Hi r/saas, I noticed many people complaining about {problem}. So I built {name} to fix it. Feedbacks welcome!",
    "IndieHackers": "Just shipped {name}. It addresses {problem} using an autonomous approach. Thoughts?",
    "ProductHunt": "Meet {name}: The autonomous solution for {problem}. No more manual work!",
    "Substack": "Why {name} is the future of solving {problem}. Read more about our autonomous roadmap."
}

async def run_growth(db: Session):
    log = models.EngineLog(level="info", source="Growth", message="Growth engine started (Gen-4 Enhanced Multi-Stage)")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Growth", message="No products to promote."))
        db.commit()
        return

    os.makedirs("growth_outbox", exist_ok=True)
    stages = ["Pre-Launch", "Launch", "Post-Launch"]

    for product in products:
        safe_name = product.name.lower().replace(" ", "_").replace("/", "_")

        for stage in stages:
            stage_dir = f"growth_outbox/{safe_name}/{stage.lower().replace('-', '_')}"
            if os.path.exists(stage_dir):
                continue

            os.makedirs(stage_dir, exist_ok=True)
            db.add(models.EngineLog(level="info", source="Growth", message=f"Generating {stage} campaign for {product.name}"))

            for channel, template in MARKETING_TEMPLATES.items():
                prompt = f"""Write a {stage} post for {channel} to promote this product:
Name: {product.name}
Description: {product.name} solves problems found in community discussions.
Using this template as inspiration: {template}
Goal: {stage} excitement and conversion.
"""
                content = await llm.generate(prompt, system=f"You are the Growth Engine Agent. Stage: {stage}.")

                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{stage_dir}/{channel.replace('/', '_')}_{timestamp}.txt"
                with open(filename, "w") as f:
                    f.write(f"CHANNEL: {channel}\nSTAGE: {stage}\nPRODUCT: {product.name}\n---\n{content}")

            db.add(models.EngineLog(level="success", source="Growth", message=f"Completed {stage} campaign for {product.name}"))

        # Simulate some traffic growth for the product
        if not db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first():
            traffic = models.TrafficLog(
                product_id=product.id,
                channel="Social Media (Simulated)",
                clicks=random.randint(50, 1000),
                signups=random.randint(5, 50)
            )
            db.add(traffic)

        if not product.is_promoted:
            product.is_promoted = True

    db.commit()
