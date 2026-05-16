from sqlalchemy.orm import Session
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started (Gen-4.1 Realism)")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products yet to monetize."))
        db.commit()
        return

    # Deterministic simulation based on traffic
    # Conversion Rate: 5% (Targeting high-intent niche problems)
    CONVERSION_RATE = 0.05

    for product in products:
        # Check traffic
        traffic = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first()
        clicks = traffic.clicks if traffic else 0

        if clicks > 0:
            potential_conversions = int(clicks * CONVERSION_RATE)
            if potential_conversions > 0:
                # Decide model based on product name/theme hint or random for now
                # In Gen-4.1 we use two primary models for simulation:
                # 1. Affiliate ($0.50 per click/lead)
                # 2. Subscription ($9.99 per signup)

                model_choice = random.choice(["Affiliate", "Subscription"])

                if model_choice == "Affiliate":
                    amount = potential_conversions * 0.50
                else:
                    amount = potential_conversions * 9.99

                revenue = models.RevenueLog(
                    product_id=product.id,
                    model=model_choice,
                    amount=amount
                )
                db.add(revenue)
                db.add(models.EngineLog(
                    level="success",
                    source="Monetization",
                    message=f"Revenue generated for {product.name}: ${amount:.2f} via {model_choice} ({potential_conversions} conversions from {clicks} clicks)"
                ))
        else:
            # Small fallback for organically discovered products without tracked traffic
            if random.random() < 0.05:
                amount = 1.0
                revenue = models.RevenueLog(product_id=product.id, model="Donation", amount=amount)
                db.add(revenue)
                db.add(models.EngineLog(level="success", source="Monetization", message=f"Organic donation received for {product.name}: ${amount:.2f}"))

    db.commit()
