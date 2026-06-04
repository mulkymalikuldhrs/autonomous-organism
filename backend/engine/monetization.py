from ..database import SessionLocal, Product, TrafficLog, LifeLog

def run_monetization():
    db = SessionLocal()
    try:
        # Process revenue for all deployed products
        products = db.query(Product).filter(Product.status == "deployed").all()
        for product in products:
            # Calculate new revenue based on clicks since last check
            # In a real scenario, we'd track 'processed' traffic logs.
            # Here, we'll simulate daily earnings from total traffic for simplicity.

            traffic = db.query(TrafficLog).filter(TrafficLog.product_id == product.id).all()
            total_clicks = sum([t.clicks for t in traffic])

            # Formula: 5% conversion rate, $10 per conversion
            # We use a deterministic calculation for Gen-4.1 stability
            expected_total_revenue = (total_clicks * 0.05) * 10

            # Add only the difference (simulating incremental daily revenue)
            current_revenue = product.revenue or 0.0
            if expected_total_revenue > current_revenue:
                incremental = expected_total_revenue - current_revenue
                product.revenue = expected_total_revenue
                db.add(LifeLog(engine="monetization", type="success", message=f"Revenue Update: +${incremental:.2f} for {product.name} (Total: ${product.revenue:.2f})"))

        db.commit()
    finally:
        db.close()
