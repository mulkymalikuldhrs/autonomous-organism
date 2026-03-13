from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started (Gen-4)")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products yet. Monetization is waiting."))
        db.commit()
        return

    models_list = ["Affiliate", "Subscription", "PPU (Pay-per-use)"]

    for product in products:
        # Simulate traffic if none exists
        traffic = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first()
        if not traffic:
            traffic = models.TrafficLog(
                product_id=product.id,
                channel="Direct/Organic",
                clicks=random.randint(100, 500),
                signups=random.randint(5, 20)
            )
            db.add(traffic)
            db.commit()

        # Simulate revenue based on signups or clicks
        # Conversion rate: 2-5% of signups buy something
        potential_buyers = max(1, int(traffic.signups * random.uniform(0.02, 0.05)))
        avg_ticket = random.uniform(9.0, 49.0)
        revenue_amount = potential_buyers * avg_ticket

        if revenue_amount > 0:
            monetization_model = random.choice(models_list)
            rev_log = models.RevenueLog(
                product_id=product.id,
                model=monetization_model,
                amount=round(revenue_amount, 2)
            )
            db.add(rev_log)

            msg = f"Revenue generated for {product.name}: ${revenue_amount:.2f} via {monetization_model}"
            db.add(models.EngineLog(level="success", source="Monetization", message=msg))
            print(msg)

    db.commit()
    db.add(models.EngineLog(level="info", source="Monetization", message="Monetization cycle complete."))
    db.commit()
