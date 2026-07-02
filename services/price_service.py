import logging
from .providers.base_provider import ProductInfo
from .providers.mercadolibre import MercadoLibreProvider

logger = logging.getLogger(__name__)

# Registro de providers disponibles — para agregar uno nuevo, solo sumarlo acá
PROVIDERS = [
    MercadoLibreProvider(),
]


def get_provider_for_url(url: str):
    """Retorna el provider adecuado para una URL dada."""
    for provider in PROVIDERS:
        if provider.can_handle(url):
            return provider
    raise ValueError(f"No hay ningún provider disponible para la URL: {url}")


def get_product_info(url: str) -> ProductInfo:
    """
    Punto de entrada principal para obtener info de precio de cualquier URL.
    El sistema elige automáticamente el provider correcto.
    """
    provider = get_provider_for_url(url)
    item_id = provider.extract_item_id(url)
    logger.info(
        f"Consultando precio para {item_id} vía {provider.__class__.__name__}")
    return provider.get_product_info(item_id)
