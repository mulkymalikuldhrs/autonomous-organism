from ..database import SessionLocal, Product, TrafficLog, LifeLog

def run_monetization():
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.status == "deployed").all()
        for product in products:
            # Calculate revenue based on clicks (simulated)
            traffic = db.query(TrafficLog).filter(TrafficLog.product_id == product.id).all()
            total_clicks = sum([t.clicks for t in traffic])

            # 5% conversion rate, $10 per conversion
            new_revenue = (total_clicks * 0.05) * 10
            product.revenue += new_revenue
            db.add(LifeLog(engine="monetization", type="success", message=f"Earned ${new_revenue} from {product.name}"))

        db.commit()
    finally:
        db.close()
