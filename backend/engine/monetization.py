from sqlalchemy.orm import Session
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products yet to monetize."))
        db.commit()
        return

    # For each product, simulate revenue if it has traffic or randomly
    # Models: Affiliate, Subscription, Jual Tools, Lead Generation, Donation
    models_available = ["Affiliate", "Subscription", "Tool Sale", "Lead Gen", "Donation"]

    for product in products:
        # Check traffic
        traffic = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first()
        clicks = traffic.clicks if traffic else 0

        # Simulation: 2% conversion rate
        potential_customers = clicks * 0.02
        if potential_customers > 0 or random.random() < 0.1: # Small chance of random sale
            model_type = random.choice(models_available)
            # Price range: $5 to $50
            amount = round(random.uniform(5.0, 50.0), 2)

            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} ({model_type})"))

    db.commit()
