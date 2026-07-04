from sqlalchemy.orm import Session
from .database import Product, User


def create_product(db: Session, user_id: int, name: str, url: str,
                   target_price: float, alert_channel: str) -> Product:
    """
    Registra un nuevo producto a monitorear.
    Valida los datos antes de insertar.
    """
    # Validaciones
    if target_price <= 0:
        raise ValueError("El precio objetivo debe ser mayor a cero")

    valid_channels = {"email", "telegram", "both"}
    if alert_channel not in valid_channels:
        raise ValueError(
            f"Canal inválido: {alert_channel}. Opciones: {valid_channels}")

    if not url or "mercadolibre" not in url.lower():
        raise ValueError("La URL debe pertenecer a Mercado Libre")

    # Verificar que el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"No existe un usuario con id={user_id}")

    product = Product(
        user_id=user_id,
        name=name,
        url=url,
        target_price=target_price,
        alert_channel=alert_channel,
        active=True
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_active_products(db: Session) -> list[Product]:
    """Retorna todos los productos activos para el ciclo de monitoreo."""
    return db.query(Product).filter(Product.active == True).all()


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    """Retorna un producto por su ID."""
    return db.query(Product).filter(Product.id == product_id).first()


def deactivate_product(db: Session, product_id: int) -> bool:
    """Desactiva un producto para que deje de monitorearse."""
    product = get_product_by_id(db, product_id)
    if not product:
        return False
    product.active = False
    db.commit()
    return True


def validate_user_alert_channel(db: Session, user_id: int, alert_channel: str) -> None:
    """
    Valida que el usuario tenga configurado el dato de contacto
    necesario para el canal de alerta elegido.
    Lanza ValueError si falta el dato requerido.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"No existe un usuario con id={user_id}")

    if alert_channel in ("email", "both") and not user.email:
        raise ValueError(
            "El canal email requiere que el usuario tenga un email configurado")

    if alert_channel in ("telegram", "both") and not user.telegram_chat_id:
        raise ValueError(
            "El canal telegram requiere que el usuario tenga un telegram_chat_id configurado")
