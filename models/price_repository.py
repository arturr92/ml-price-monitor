from sqlalchemy.orm import Session
from datetime import datetime
from .database import PriceHistory, Product


def save_price_record(db: Session, product_id: int, price: float) -> PriceHistory | None:
    """
    Guarda un nuevo registro de precio en PRICE_HISTORY.
    Evita duplicados si el precio no cambió en el mismo ciclo (última hora).
    """
    # Verificar si ya existe un registro reciente con el mismo precio
    one_hour_ago = datetime.now().replace(minute=0, second=0, microsecond=0)
    existing = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.price == price,
        PriceHistory.checked_at >= one_hour_ago
    ).first()

    if existing:
        return None  # Ya hay un registro igual en este ciclo, no duplicar

    record = PriceHistory(
        product_id=product_id,
        price=price,
        checked_at=datetime.now()
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_price_history(db: Session, product_id: int, limit: int = 50) -> list[PriceHistory]:
    """Retorna el historial de precios de un producto, ordenado por fecha descendente."""
    return (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.checked_at.desc())
        .limit(limit)
        .all()
    )


def get_latest_price(db: Session, product_id: int) -> PriceHistory | None:
    """Retorna el precio más reciente de un producto."""
    return (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.checked_at.desc())
        .first()
    )
