from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime

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
    channels = ["Twitter/X", "Reddit", "IndieHackers", "Medium"]

    for product in unpromoted:
        db.add(models.EngineLog(level="info", source="Growth", message=f"Starting promotion for {product.name}"))

        for channel in channels:
            # Generate promo content using LLM
            prompt = f"Write a catchy {channel} post to launch this product:\nName: {product.name}\nGoal: Attract early adopters and solve their pain points."
            promo_text = await llm.generate(prompt, system="You are the Growth Engine Agent specialized in digital marketing.")

            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_name = product.name.lower().replace(" ", "_").replace("/", "_")
            content_file = f"growth_outbox/{safe_name}_{channel.replace('/', '_')}_{timestamp}.txt"

            with open(content_file, "w") as f:
                f.write(f"CHANNEL: {channel}\nPRODUCT: {product.name}\nDATE: {timestamp}\n---\n{promo_text}")

            # Simulate distribution success
            db.add(models.EngineLog(level="success", source="Growth", message=f"Promoted {product.name} on {channel}. Content: {content_file}"))

        # Mark as promoted
        product.is_promoted = True
        db.add(models.EngineLog(level="info", source="Growth", message=f"Promotion cycle complete for {product.name}"))

    db.commit()
    return {"promoted_count": len(unpromoted)}
