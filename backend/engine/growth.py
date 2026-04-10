from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import os
import datetime
import random

async def run_growth(db: Session):
    log = models.EngineLog(level="info", source="Growth", message="Growth engine started (Gen-4 Multi-Channel)")
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

    platforms = {
        "Twitter/X": "Write a short, viral-style tweet with hashtags.",
        "Reddit": "Write a helpful, community-focused post for r/SaaS or r/startups.",
        "IndieHackers": "Write a transparent 'build in public' update.",
        "Telegram": "Write a quick announcement for an Indonesian tech group."
    }

    for product in products:
        safe_name = product.name.lower().replace(" ", "_").replace("/", "_")

        # Determine stage: if already promoted, move to next stage or stay at Post-Launch
        current_stage = "Pre-Launch"
        if product.is_promoted:
            # Check logs to see if we already did Pre-Launch
            done_pre = db.query(models.EngineLog).filter(
                models.EngineLog.source == "Growth",
                models.EngineLog.message.contains(f"Pre-Launch campaign for {product.name}")
            ).first()
            if done_pre:
                current_stage = "Launch"

            done_launch = db.query(models.EngineLog).filter(
                models.EngineLog.source == "Growth",
                models.EngineLog.message.contains(f"Launch campaign for {product.name}")
            ).first()
            if done_launch:
                current_stage = "Post-Launch"

        stage_dir = f"growth_outbox/{safe_name}/{current_stage.lower().replace('-', '_')}"
        if os.path.exists(stage_dir):
            # Already generated for this stage, simulate traffic
            traffic = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first()
            if not traffic:
                traffic = models.TrafficLog(product_id=product.id, clicks=0, signups=0)
                db.add(traffic)

            new_clicks = random.randint(10, 50)
            traffic.clicks += new_clicks
            db.add(models.EngineLog(level="info", source="Growth", message=f"Traffic surge: +{new_clicks} clicks for {product.name} from {current_stage} campaign."))
            db.commit()
            continue

        os.makedirs(stage_dir, exist_ok=True)
        db.add(models.EngineLog(level="info", source="Growth", message=f"Generating {current_stage} campaign for {product.name}"))

        for channel, instruction in platforms.items():
            prompt = f"""{instruction}
Product: {product.name}
Description: {product.name} solves human problems identified by the Autonomous Organism.
Stage: {current_stage}
Target: Early adopters and people looking for automated solutions.
"""
            content = await llm.generate(prompt, system=f"You are the Growth Engine Agent. You are an expert marketer. You speak English and Indonesian if the channel is Telegram.")

            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{stage_dir}/{channel.replace('/', '_')}_{timestamp}.txt"
            with open(filename, "w") as f:
                f.write(f"CHANNEL: {channel}\nSTAGE: {current_stage}\nPRODUCT: {product.name}\n---\n{content}")

        product.is_promoted = True
        db.add(models.EngineLog(level="success", source="Growth", message=f"Completed {current_stage} campaign for {product.name}"))

        # Initial traffic boost
        traffic = models.TrafficLog(product_id=product.id, clicks=random.randint(50, 200), signups=random.randint(1, 5))
        db.add(traffic)

    db.commit()
