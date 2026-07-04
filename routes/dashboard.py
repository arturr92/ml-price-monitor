from flask import Blueprint, render_template
from models.database import SessionLocal
from models.product_repository import get_active_products
from models.price_repository import get_latest_price
from models.alert_repository import get_alerts_sent

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
def dashboard():
    db = SessionLocal()
    try:
        products = get_active_products(db)
        products_data = []

        for product in products:
            latest = get_latest_price(db, product.id)
            last_alert = get_alerts_sent(db, product.id, limit=1)

            products_data.append({
                "id": product.id,
                "name": product.name,
                "url": product.url,
                "target_price": product.target_price,
                "current_price": latest.price if latest else None,
                "alert_channel": product.alert_channel,
                "alert_sent": len(last_alert) > 0,
                "last_checked": latest.checked_at if latest else None,
            })

        return render_template("dashboard.html", products=products_data)
    finally:
        db.close()
