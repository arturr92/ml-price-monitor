from .logger import setup_logger
import logging
import os
from dotenv import load_dotenv
from .providers.base_provider import ProductInfo
from .providers.mercadolibre import MercadoLibreProvider
from .providers.mock_provider import MockProvider

load_dotenv()

logger = setup_logger(__name__)


def get_provider_for_url(url: str):
    use_mock = os.getenv("USE_MOCK", "False").lower() == "true"
    providers = [MockProvider() if use_mock else MercadoLibreProvider()]
    for provider in providers:
        if provider.can_handle(url):
            return provider
    raise ValueError(f"No hay ningún provider disponible para la URL: {url}")


def get_product_info(url: str) -> ProductInfo:
    provider = get_provider_for_url(url)
    item_id = provider.extract_item_id(url)
    logger.info(
        f"Consultando precio para {item_id} vía {provider.__class__.__name__}")
    return provider.get_product_info(item_id)
