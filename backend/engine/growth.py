from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import asyncio

async def simulate_marketing_push(product_name: str, content: str):
    # Simulate finding users and posting content
    channels = ["Twitter/X", "Reddit", "IndieHackers", "LinkedIn"]
    for channel in channels:
        await asyncio.sleep(0.5)
        print(f"[GROWTH] Posting {product_name} to {channel}...")
    return True

async def run_growth(db: Session):
    log = models.EngineLog(level="info", source="Growth", message="Growth engine started")
    db.add(log)
    db.commit()

    # Get unprocessed products
    unpromoted = db.query(models.Product).filter(models.Product.is_promoted == False).all()
    if not unpromoted:
        db.add(models.EngineLog(level="info", source="Growth", message="No new products to promote."))
        db.commit()
        return

    os.makedirs("growth_outbox", exist_ok=True)

    for product in unpromoted:
        # Generate promo content using LLM
        prompt = f"Write a catchy social media post to launch this product:\nName: {product.name}\nBlueprint path: {product.blueprint_path}"
        promo_text = await llm.generate(prompt, system="You are the Growth Engine Agent.")

        content_file = f"growth_outbox/promo_{product.id}_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
        with open(content_file, "w") as f:
            f.write(promo_text)

        # SIMULATE MARKETING
        db.add(models.EngineLog(level="info", source="Growth", message=f"Initiating marketing push for {product.name}..."))
        db.commit()

        await simulate_marketing_push(product.name, promo_text)

        # Mark as promoted
        product.is_promoted = True
        db.add(models.EngineLog(level="success", source="Growth", message=f"Marketing completed for {product.name}. Reach increasing."))

    db.commit()
