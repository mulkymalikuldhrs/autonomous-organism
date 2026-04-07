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

        # Simulation: Fixed 2% conversion rate and $19 price per conversion
        # This replaces the previous random probability logic for more deterministic simulation
        conversion_rate = 0.02
        price_per_conversion = 19.0
        conversions = int(clicks * conversion_rate)

        if conversions > 0:
            model_type = random.choice(models_available)
            total_amount = round(conversions * price_per_conversion, 2)

            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=total_amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${total_amount} ({conversions} conversions via {model_type})"))

    db.commit()
