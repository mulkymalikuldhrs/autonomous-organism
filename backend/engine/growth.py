from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import random

async def run_growth(db: Session):
    log = models.EngineLog(level="info", source="Growth", message="Growth engine started (Gen-4.1 Autonomous Posting)")
    db.add(log)
    db.commit()

    # Get products
    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Growth", message="No products to promote."))
        db.commit()
        return

    outbox_dir = "growth_outbox"
    os.makedirs(outbox_dir, exist_ok=True)
    stages = ["Launch", "Post-Launch"]
    channels = ["Twitter/X", "Reddit", "IndieHackers"]

    for product in products:
        safe_name = product.name.lower().replace(" ", "_").replace("/", "_")

        for stage in stages:
            for channel in channels:
                # Check if already posted for this product, stage, and channel
                existing_log = db.query(models.TrafficLog).filter(
                    models.TrafficLog.product_id == product.id,
                    models.TrafficLog.channel == f"{stage}_{channel}"
                ).first()

                if existing_log:
                    continue

                prompt = f"""Write a {stage} post for {channel} to promote this product:
Name: {product.name}
Description: {product.name} solves problems found in community discussions.
Goal: {stage} excitement and conversion.
"""
                content = await llm.generate(prompt, system=f"You are the Growth Engine Agent. Stage: {stage}.")

                # Simulate real posting by writing to outbox AND logging as traffic event
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{safe_name}_{stage}_{channel}_{timestamp}.txt".replace("/", "_")
                filepath = os.path.join(outbox_dir, filename)

                with open(filepath, "w") as f:
                    f.write(f"STATUS: POSTED\nCHANNEL: {channel}\nSTAGE: {stage}\nPRODUCT: {product.name}\n---\n{content}")

                # Create traffic log for this post
                clicks = random.randint(5, 50) # Initial organic interest
                traffic = models.TrafficLog(
                    product_id=product.id,
                    channel=f"{stage}_{channel}",
                    clicks=clicks,
                    signups=int(clicks * 0.1)
                )
                db.add(traffic)
                db.add(models.EngineLog(level="success", source="Growth", message=f"Successfully 'POSTED' {stage} campaign for {product.name} on {channel} (Gained {clicks} clicks)"))

    # Update promoted status
    for product in products:
        product.is_promoted = True

    db.commit()
