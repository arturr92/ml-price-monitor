import re
import logging
import requests
import os
from datetime import datetime
from time import sleep
from .base_provider import BaseProvider, ProductInfo

from ..logger import setup_logger
logger = setup_logger(__name__)

ML_API_BASE = "https://api.mercadolibre.com"
REQUEST_TIMEOUT = 10      # segundos
MAX_RETRIES = 2
RETRY_BACKOFF = 2         # segundos entre reintentos


class MercadoLibreProvider(BaseProvider):

    def can_handle(self, url: str) -> bool:
        return "mercadolibre" in url.lower()

    def extract_item_id(self, url: str) -> str:
        if not url or not self.can_handle(url):
            raise ValueError(
                f"URL inválida o no pertenece a Mercado Libre: {url}")

        match = re.search(r'(ML[A-Z])-?(\d+)', url.upper())
        if not match:
            raise ValueError(
                f"No se encontró un item_id válido en la URL: {url}")

        return match.group(1) + match.group(2)

    def get_product_info(self, item_id: str) -> ProductInfo:
        url = f"{ML_API_BASE}/items/{item_id}"

        for attempt in range(1, MAX_RETRIES + 2):
            try:
                response = requests.get(
                    url,
                    timeout=REQUEST_TIMEOUT,
                    headers={
                        "Authorization": f"Bearer {os.getenv('ML_ACCESS_TOKEN', '')}",
                        "Accept": "application/json",
                    }
                )

                if response.status_code == 404:
                    raise ValueError(f"Producto {item_id} no encontrado en ML")

                response.raise_for_status()
                data = response.json()

                return ProductInfo(
                    item_id=item_id,
                    title=data.get("title", "Sin título"),
                    price=float(data.get("price", 0)),
                    currency=data.get("currency_id", "ARS"),
                    available=data.get("status") == "active",
                    source="mercadolibre",
                    fetched_at=datetime.now()
                )

            except ValueError:
                raise
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout en intento {attempt} para {item_id}")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Error de conexión en intento {attempt}: {e}")

            if attempt <= MAX_RETRIES:
                sleep(RETRY_BACKOFF * attempt)

        raise ConnectionError(
            f"No se pudo obtener precio de {item_id} tras {MAX_RETRIES + 1} intentos")
