from datetime import datetime
from .base_provider import BaseProvider, ProductInfo

# Catálogo de productos simulados para desarrollo
MOCK_PRODUCTS = {
    "MLA123456789": ProductInfo(
        item_id="MLA123456789",
        title="Notebook Lenovo IdeaPad - MOCK",
        price=150000.0,
        currency="ARS",
        available=True,
        source="mock",
        fetched_at=datetime.now()
    ),
    "MLA987654321": ProductInfo(
        item_id="MLA987654321",
        title="iPhone 15 Pro Max - MOCK",
        price=2500000.0,
        currency="ARS",
        available=True,
        source="mock",
        fetched_at=datetime.now()
    ),
    "MLA111111111": ProductInfo(
        item_id="MLA111111111",
        title="Samsung TV 55\" - MOCK",
        price=800000.0,
        currency="ARS",
        available=False,
        source="mock",
        fetched_at=datetime.now()
    ),
}


class MockProvider(BaseProvider):
    """
    Provider de desarrollo — simula respuestas de la API sin hacer requests reales.
    Usar solo cuando USE_MOCK=True en .env.
    Reemplazar por MercadoLibreProvider cuando el token esté disponible.
    """

    def can_handle(self, url: str) -> bool:
        return "mercadolibre" in url.lower()

    def extract_item_id(self, url: str) -> str:
        import re
        if not url or not self.can_handle(url):
            raise ValueError(f"URL inválida: {url}")
        match = re.search(r'(ML[A-Z])-?(\d+)', url.upper())
        if not match:
            raise ValueError(f"No se encontró item_id en: {url}")
        return match.group(1) + match.group(2)

    def get_product_info(self, item_id: str) -> ProductInfo:
        if item_id not in MOCK_PRODUCTS:
            raise ValueError(f"Producto {item_id} no encontrado en mock")
        # Simulamos variación de precio para que el monitor detecte cambios
        import random
        product = MOCK_PRODUCTS[item_id]
        variation = random.uniform(-0.05, 0.05)  # ±5%
        return ProductInfo(
            item_id=product.item_id,
            title=product.title,
            price=round(product.price * (1 + variation), 2),
            currency=product.currency,
            available=product.available,
            source=product.source,
            fetched_at=datetime.now()
        )
