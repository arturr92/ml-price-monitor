from flask import Blueprint, render_template, abort
from models.database import SessionLocal
from models.product_repository import get_product_by_id
from models.price_repository import get_price_history
from models.alert_repository import get_alerts_sent

history_bp = Blueprint("history", __name__)


@history_bp.route("/product/<int:product_id>")
def product_history(product_id):
    db = SessionLocal()
    try:
        product = get_product_by_id(db, product_id)
        if not product:
            abort(404)

        history = get_price_history(db, product_id, limit=50)
        alerts = get_alerts_sent(db, product_id, limit=10)

        # Preparar datos para el gráfico
        labels = [h.checked_at.strftime("%d/%m %H:%M")
                  for h in reversed(history)]
        prices = [h.price for h in reversed(history)]

        return render_template(
            "product_history.html",
            product=product,
            history=history,
            alerts=alerts,
            labels=labels,
            prices=prices,
        )
    finally:
        db.close()
