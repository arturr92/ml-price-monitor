from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .database import AlertSent, Product


def register_alert_sent(
    db: Session,
    product_id: int,
    price_at_alert: float,
    channel_used: str
) -> AlertSent:
    """Registra una alerta enviada en la base de datos."""
    alert = AlertSent(
        product_id=product_id,
        price_at_alert=price_at_alert,
        channel_used=channel_used,
        sent_at=datetime.now()
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def should_send_alert(
    db: Session,
    product_id: int,
    current_price: float,
    target_price: float
) -> bool:
    """
    Determina si se debe enviar una alerta para un producto.
    Reglas:
    - El precio actual debe ser menor o igual al precio objetivo
    - No se envía si ya se notificó ese mismo precio anteriormente
    - Sí se envía si el precio bajó aún más desde la última alerta
    """
    if current_price > target_price:
        return False

    last_alert = (
        db.query(AlertSent)
        .filter(AlertSent.product_id == product_id)
        .order_by(AlertSent.sent_at.desc())
        .first()
    )

    if not last_alert:
        return True  # Primera alerta para este producto

    # Enviar solo si el precio bajó más que en la última alerta
    return current_price < last_alert.price_at_alert


def get_alerts_sent(db: Session, product_id: int, limit: int = 20) -> list[AlertSent]:
    """Retorna el historial de alertas enviadas para un producto."""
    return (
        db.query(AlertSent)
        .filter(AlertSent.product_id == product_id)
        .order_by(AlertSent.sent_at.desc())
        .limit(limit)
        .all()
    )
