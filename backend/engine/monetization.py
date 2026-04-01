from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import random
import datetime

MONETIZATION_MODELS = ["Subscription", "Affiliate", "Pay-as-you-go", "Donation"]

async def run_monetization(db: Session):
    log_source = "Monetization"
    db.add(models.EngineLog(level="info", source=log_source, message="Monetization Engine analyzing performance"))
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source=log_source, message="No products to monetize yet."))
        db.commit()
        return

    for product in products:
        # Determine the best model using LLM if not already set (simulation)
        model = random.choice(MONETIZATION_MODELS)

        # 1. Traffic simulation for each product
        # Each product gets some base traffic
        new_clicks = random.randint(10, 100)
        new_signups = random.randint(0, int(new_clicks * 0.1)) # 10% max signup rate

        traffic = models.TrafficLog(
            product_id=product.id,
            channel=random.choice(["Twitter", "Reddit", "Organic"]),
            clicks=new_clicks,
            signups=new_signups
        )
        db.add(traffic)

        # 2. Revenue simulation based on signups
        # 5% conversion from signup to paid
        paid_users = int(new_signups * 0.05)
        if paid_users > 0:
            amount = paid_users * random.uniform(10.0, 50.0) # $10-$50 per user
            revenue = models.RevenueLog(
                product_id=product.id,
                model=model,
                amount=amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source=log_source, message=f"Generated ${amount:.2f} revenue from {product.name} ({model})"))

    db.commit()
