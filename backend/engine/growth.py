from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime

async def run_growth(db: Session):
    log = models.EngineLog(level="info", source="Growth", message="Growth engine started (Gen-4 Multi-Stage)")
    db.add(log)
    db.commit()

    # Get products
    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Growth", message="No products to promote."))
        db.commit()
        return

    os.makedirs("growth_outbox", exist_ok=True)
    stages = ["Pre-Launch", "Launch", "Post-Launch"]
    channels = ["Twitter/X", "Reddit", "IndieHackers", "Kaskus", "Quora ID"]

    for product in products:
        # Determine current stage based on product age or logs
        # For simplicity, let's generate content for all stages if not already done
        safe_name = product.name.lower().replace(" ", "_").replace("/", "_")

        for stage in stages:
            stage_dir = f"growth_outbox/{safe_name}/{stage.lower().replace('-', '_')}"
            if os.path.exists(stage_dir):
                continue # Skip if already generated

            os.makedirs(stage_dir, exist_ok=True)
            db.add(models.EngineLog(level="info", source="Growth", message=f"Generating {stage} campaign for {product.name}"))

            for channel in channels:
                prompt = f"""Write a {stage} post for {channel} to promote this product:
Name: {product.name}
Description: {product.name} solves problems found in community discussions.
Goal: {stage} excitement and conversion.
"""
                content = await llm.generate(prompt, system=f"You are the Growth Engine Agent. Stage: {stage}.")

                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{stage_dir}/{channel.replace('/', '_')}_{timestamp}.txt"
                with open(filename, "w") as f:
                    f.write(f"CHANNEL: {channel}\nSTAGE: {stage}\nPRODUCT: {product.name}\n---\n{content}")

            db.add(models.EngineLog(level="success", source="Growth", message=f"Completed {stage} campaign for {product.name}"))

    # Update promoted status and simulate traffic
    for product in products:
        if not product.is_promoted:
            product.is_promoted = True
            # Initial traffic injection
            traffic = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first()
            if not traffic:
                traffic = models.TrafficLog(product_id=product.id, channel="Organic", clicks=0)
                db.add(traffic)
            traffic.clicks += 50

    db.commit()
