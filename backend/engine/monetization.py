from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started (Gen-4 Revenue Simulator)")
    db.add(log)
    db.commit()

    # Get active products
    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products found to monetize."))
        db.commit()
        return

    models_list = ["Affiliate", "Subscription", "Tools Sale", "Lead Gen", "Donation"]

    for product in products:
        # Simulate traffic based on is_promoted
        base_clicks = random.randint(10, 50)
        if product.is_promoted:
            base_clicks *= 5 # 5x more clicks if promoted

        traffic = models.TrafficLog(
            product_id=product.id,
            channel=random.choice(["Twitter/X", "Reddit", "IndieHackers"]),
            clicks=base_clicks,
            signups=int(base_clicks * random.uniform(0.01, 0.05))
        )
        db.add(traffic)

        # Simulate revenue based on signups
        if traffic.signups > 0:
            conv_rate = random.uniform(0.05, 0.15)
            buyers = int(traffic.signups * conv_rate)
            if buyers > 0 or random.random() < 0.1: # Even with 0 buyers, 10% chance of random small income
                model = random.choice(models_list)
                amount = round(random.uniform(5.0, 49.0) * (buyers if buyers > 0 else 1), 2)

                revenue = models.RevenueLog(
                    product_id=product.id,
                    model=model,
                    amount=amount
                )
                db.add(revenue)
                db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} via {model}"))

    db.commit()
