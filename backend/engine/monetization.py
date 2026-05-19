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

    # For each product, simulate revenue based on traffic
    # Deterministic conversion rate: 5%
    conversion_rate = 0.05

    monetization_config = {
        "Affiliate": {"price": 0.50, "unit": "click"},
        "Subscription": {"price": 9.99, "unit": "signup"},
        "Tool Sale": {"price": 29.00, "unit": "sale"},
        "Lead Gen": {"price": 5.00, "unit": "lead"},
        "Donation": {"price": 2.00, "unit": "coffee"}
    }

    for product in products:
        # Check traffic
        traffic_logs = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).all()
        total_clicks = sum(log.clicks for log in traffic_logs) if traffic_logs else 0

        if total_clicks > 0:
            # Calculate conversions
            conversions = int(total_clicks * conversion_rate)
            if conversions > 0:
                model_type = random.choice(list(monetization_config.keys()))
                config = monetization_config[model_type]
                amount = round(conversions * config["price"], 2)

                revenue = models.RevenueLog(
                    product_id=product.id,
                    model=model_type,
                    amount=amount
                )
                db.add(revenue)
                db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} via {conversions} {config['unit']}s ({model_type})"))
        elif random.random() < 0.05: # 5% chance of organic sale even without tracked clicks
            model_type = random.choice(list(monetization_config.keys()))
            amount = monetization_config[model_type]["price"]
            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Organic revenue for {product.name}: ${amount} ({model_type})"))

    db.commit()
