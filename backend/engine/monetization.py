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
        clicks = traffic.clicks if traffic else random.randint(0, 100) # Fallback to some simulated traffic

        # Determine revenue model based on product name/theme hint
        name_lower = product.name.lower()
        if "tool" in name_lower or "app" in name_lower:
            model_type = "Tool Sale"
            conversion_rate = 0.03
            price = 29.0
        elif "service" in name_lower or "agency" in name_lower:
            model_type = "Subscription"
            conversion_rate = 0.01
            price = 49.0
        elif "lead" in name_lower or "find" in name_lower:
            model_type = "Lead Gen"
            conversion_rate = 0.05
            price = 5.0
        else:
            model_type = random.choice(models_available)
            conversion_rate = 0.02
            price = 19.0

        # Deterministic simulation: conversion based on clicks
        sales_count = int(clicks * conversion_rate)

        # Ensure at least some activity if there's significant traffic
        if sales_count == 0 and clicks > 20 and random.random() < 0.3:
            sales_count = 1

        if sales_count > 0:
            total_amount = round(sales_count * price, 2)
            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=total_amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${total_amount} from {sales_count} sales ({model_type})"))

    db.commit()
