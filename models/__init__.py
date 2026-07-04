from .database import Base, engine, SessionLocal, get_db
from .database import User, Product, PriceHistory, AlertSent
from .price_repository import save_price_record, get_price_history, get_latest_price

from .product_repository import (
    create_product, get_active_products,
    get_product_by_id, deactivate_product
)

from .product_repository import (
    create_product, get_active_products,
    get_product_by_id, deactivate_product,
    validate_user_alert_channel
)

from .alert_repository import register_alert_sent, should_send_alert, get_alerts_sent
