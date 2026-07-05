import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from .base_provider import BaseProvider, ProductInfo
from ..logger import setup_logger

logger = setup_logger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-AR,es;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}
REQUEST_TIMEOUT = 15


class MLScrapingProvider(BaseProvider):
    """
    Provider de scraping directo para Mercado Libre.
    No requiere autenticación — extrae el precio de la página del producto.
    Se usa como fallback cuando la API oficial no está disponible.
    """

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
        url = f"https://www.mercadolibre.com.ar/p/{item_id}"
        try:
            response = requests.get(
                url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            # Extraer título
            title = self._extract_title(soup)

            # Extraer precio
            price = self._extract_price(soup)

            if not price:
                raise ValueError(f"No se pudo extraer el precio de {item_id}")

            logger.info(f"Scraping exitoso para {item_id} — precio: ${price}")

            return ProductInfo(
                item_id=item_id,
                title=title or "Sin título",
                price=price,
                currency="ARS",
                available=True,
                source="ml_scraping",
                fetched_at=datetime.now()
            )

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error de conexión al hacer scraping de {item_id}: {e}")
            raise ConnectionError(
                f"No se pudo conectar a ML para {item_id}: {e}")

    def _extract_title(self, soup: BeautifulSoup) -> str:
        selectors = [
            "h1.ui-pdp-title",
            "h1",
        ]
        for selector in selectors:
            el = soup.select_one(selector)
            if el:
                return el.get_text(strip=True)
        return "Sin título"

    def _extract_price(self, soup: BeautifulSoup) -> float | None:
        selectors = [
            "span.andes-money-amount__fraction",
            "meta[itemprop='price']",
            "span[class*='price-tag-fraction']",
        ]
        for selector in selectors:
            el = soup.select_one(selector)
            if el:
                # Para meta tag
                if el.name == "meta":
                    val = el.get("content", "")
                else:
                    val = el.get_text(strip=True)

                # Limpiar y convertir
                val = val.replace(".", "").replace(",", ".").strip()
                try:
                    return float(val)
                except ValueError:
                    continue
        return None
