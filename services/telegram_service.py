import requests
import os
from dotenv import load_dotenv
from .logger import setup_logger

load_dotenv()

logger = setup_logger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_API_BASE = "https://api.telegram.org"


def send_price_alert_telegram(
    chat_id: str,
    product_name: str,
    current_price: float,
    target_price: float,
    product_url: str
) -> bool:
    """
    Envía un mensaje de alerta por Telegram cuando el precio baja del umbral.
    Retorna True si se envió correctamente, False si falló.
    """
    if not TELEGRAM_TOKEN:
        logger.warning("Token de Telegram no configurado — mensaje no enviado")
        return False

    message = (
        f"🔔 *¡Bajó el precio!*\n\n"
        f"📦 *Producto:* {product_name}\n"
        f"💰 *Precio actual:* ${current_price:,.2f}\n"
        f"🎯 *Tu precio objetivo:* ${target_price:,.2f}\n\n"
        f"[Ver producto en Mercado Libre]({product_url})"
    )

    url = f"{TELEGRAM_API_BASE}/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(
            f"Telegram enviado a chat_id={chat_id} — producto: {product_name} — precio: ${current_price}")
        return True

    except requests.exceptions.HTTPError as e:
        logger.error(
            f"Error HTTP al enviar Telegram: {e} — respuesta: {response.text}")
        return False
    except requests.exceptions.Timeout:
        logger.error("Timeout al enviar mensaje de Telegram")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al enviar Telegram: {e}")
        return False
