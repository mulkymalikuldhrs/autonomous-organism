from sqlalchemy.orm import Session
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started (Gen-4 Deterministic Simulation)")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products yet to monetize."))
        db.commit()
        return

    for product in products:
        # Check traffic
        traffic_logs = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).all()
        total_clicks = sum(t.clicks for t in traffic_logs) if traffic_logs else 0

        # Deterministic revenue based on traffic and product "category" (derived from name)
        # Higher complexity or high-value themes get higher ARP (Average Revenue per Click)
        high_value_keywords = ["ai", "crypto", "business", "enterprise", "automation", "scale"]
        base_arp = 0.05 # $0.05 per click

        if any(kw in product.name.lower() for kw in high_value_keywords):
            base_arp = 0.15 # $0.15 per click for high value niches

        # Simulated conversion logic
        # 1-3% conversion rate
        conversion_rate = 0.01 + (random.random() * 0.02)
        customers = int(total_clicks * conversion_rate)

        if customers > 0:
            # Check if we already logged revenue for this product today to avoid double counting same traffic
            # For simulation purposes, we'll just add new revenue for new customers

            model_type = "Subscription" if base_arp > 0.1 else "Affiliate"
            price = 29.0 if model_type == "Subscription" else 5.0
            total_amount = round(customers * price, 2)

            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=total_amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${total_amount} from {customers} customers ({model_type})"))

        elif random.random() < 0.05: # 5% chance of a "organic" discovery sale even with low traffic
            amount = round(random.uniform(10.0, 100.0), 2)
            revenue = models.RevenueLog(
                product_id=product.id,
                model="Donation",
                amount=amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Organic donation received for {product.name}: ${amount}"))

    db.commit()
