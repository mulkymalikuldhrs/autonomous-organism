from sqlalchemy.orm import Session
from .. import models
import random
import datetime
import json
import os

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started (Gen-4.1 Deterministic Mode)")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products yet to monetize."))
        db.commit()
        return

    for product in products:
        # Load blueprint to understand monetization model
        model_type = "Subscription"
        if product.blueprint_path and os.path.exists(product.blueprint_path):
            with open(product.blueprint_path, 'r') as f:
                spec = json.load(f)
                model_hint = spec.get('spec', {}).get('monetization_model', '')
                if 'Affiliate' in model_hint: model_type = "Affiliate"
                elif 'Donasi' in model_hint or 'Donation' in model_hint: model_type = "Donation"

        # Check traffic
        traffic = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first()
        clicks = traffic.clicks if traffic else 0

        # Deterministic Simulation based on traffic
        # 1-3% conversion rate
        conversion_rate = 0.02
        customers = int(clicks * conversion_rate)

        if customers > 0:
            avg_price = 19.99 if model_type == "Subscription" else (4.99 if model_type == "Donation" else 12.50)
            amount = round(customers * avg_price, 2)

            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Deterministic revenue generated for {product.name}: ${amount} ({model_type}) from {clicks} clicks"))

    db.commit()
