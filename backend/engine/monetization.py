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
        clicks = traffic.clicks if traffic else random.randint(10, 100) # Simulate some traffic if missing

        # Simulation: 5% conversion rate for realistic testing
        potential_customers = clicks * 0.05
        if potential_customers >= 1 or random.random() < 0.3:
            model_type = random.choice(models_available)
            # Price range: Affiliate ($0.50) to Subscription ($9.99)
            if model_type == "Affiliate":
                amount = round(clicks * 0.50, 2)
            elif model_type == "Subscription":
                amount = 9.99
            else:
                amount = round(random.uniform(5.0, 50.0), 2)

            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} ({model_type})"))

    db.commit()
