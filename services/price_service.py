import logging
import os
from dotenv import load_dotenv
from .providers.base_provider import ProductInfo
from .providers.mercadolibre import MercadoLibreProvider
from .providers.mock_provider import MockProvider
from .providers.ml_scraping_provider import MLScrapingProvider
from .logger import setup_logger

load_dotenv()

logger = setup_logger(__name__)

USE_MOCK = os.getenv("USE_MOCK", "False").lower() == "true"


def get_provider_for_url(url: str):
    if USE_MOCK:
        providers = [MockProvider()]
    else:
        providers = [
            MercadoLibreProvider(),     # 1° intento: API oficial
            MLScrapingProvider(),        # 2° intento: scraping como fallback
        ]
    for provider in providers:
        if provider.can_handle(url):
            return provider
    raise ValueError(f"No hay ningún provider disponible para la URL: {url}")


def get_product_info(url: str) -> ProductInfo:
    if USE_MOCK:
        provider = get_provider_for_url(url)
        item_id = provider.extract_item_id(url)
        logger.info(
            f"Consultando precio para {item_id} vía {provider.__class__.__name__}")
        return provider.get_product_info(item_id)

    # Con providers reales, intentamos en orden y hacemos fallback
    item_id = None
    last_error = None

    if "mercadolibre" in url.lower():
        providers_to_try = [MercadoLibreProvider(), MLScrapingProvider()]
    else:
        raise ValueError(
            f"No hay ningún provider disponible para la URL: {url}")

    for provider in providers_to_try:
        try:
            item_id = provider.extract_item_id(url)
            logger.info(
                f"Consultando precio para {item_id} vía {provider.__class__.__name__}")
            return provider.get_product_info(item_id)
        except Exception as e:
            logger.warning(
                f"{provider.__class__.__name__} falló: {e} — intentando siguiente provider")
            last_error = e
            continue

    raise ConnectionError(
        f"Todos los providers fallaron para {url}. Último error: {last_error}")
