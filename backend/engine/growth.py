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

    for product in unpromoted:
        # Generate promo content using LLM
        prompt = f"Write catchy social media posts (Twitter, Reddit, IndieHackers) to launch this product:\nName: {product.name}\nBlueprint path: {product.blueprint_path}"
        promo_text = await llm.generate(prompt, system="You are the Growth Engine Agent.")

        content_file = f"growth_outbox/promo_{product.id}_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
        with open(content_file, "w") as f:
            f.write(promo_text)

        # Mark as promoted
        product.is_promoted = True
        db.add(models.EngineLog(level="info", source="Growth", message=f"Generated promo for {product.name}: {content_file}"))

    # NOTE: Real tracking logic requires external API integrations (e.g., Stripe, Twitter API).
    # The organism is designed to ingest real traffic data from webhooks or API polling.
    # Currently, it logs the marketing push and waits for external conversion signals.
    db.add(models.EngineLog(level="info", source="Growth", message="Marketing content deployed to outbox. Ready for real-world ingestion."))

    db.commit()
