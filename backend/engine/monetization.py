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
        # Aggregate clicks for the product
        total_clicks = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).with_entities(models.TrafficLog.clicks).all()
        clicks = sum([c[0] for c in total_clicks])

        # Simulation: 5% conversion rate (deterministic for real-data simulation)
        # We use a conversion factor to generate revenue entries
        conversion_rate = 0.05
        sales_count = int(clicks * conversion_rate)

        if sales_count > 0:
            for _ in range(sales_count):
                model_type = random.choice(models_available)
                # Deterministic simulation based on model
                if model_type == "Affiliate":
                    amount = 0.50 # per click/lead
                elif model_type == "Subscription":
                    amount = 9.99
                else:
                    amount = round(random.uniform(5.0, 20.0), 2)

                revenue = models.RevenueLog(
                    product_id=product.id,
                    model=model_type,
                    amount=amount
                )
                db.add(revenue)
                db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} ({model_type})"))

    db.commit()
