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
        # Check traffic (sum of clicks across all channels)
        clicks_data = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).all()
        total_clicks = sum(t.clicks for t in clicks_data) if clicks_data else 0

        # Simulation: 5% conversion rate for realistic testing
        conversion_rate = 0.05
        potential_sales = int(total_clicks * conversion_rate)

        if potential_sales > 0:
            for _ in range(potential_sales):
                model_type = random.choice(models_available)

                # Deterministic revenue based on model type
                if model_type == "Affiliate":
                    amount = 0.50 # per click/lead
                elif model_type == "Subscription":
                    amount = 9.99 # per signup
                elif model_type == "Tool Sale":
                    amount = 29.00 # one-time
                else:
                    amount = round(random.uniform(1.0, 5.0), 2)

                revenue = models.RevenueLog(
                    product_id=product.id,
                    model=model_type,
                    amount=amount
                )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} ({model_type})"))

    db.commit()
