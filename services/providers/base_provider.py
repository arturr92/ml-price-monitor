from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductInfo:
    """Estructura estandarizada de respuesta para cualquier provider."""
    item_id: str
    title: str
    price: float
    currency: str
    available: bool
    source: str           # "mercadolibre", "amazon", etc.
    fetched_at: datetime


class BaseProvider(ABC):
    """
    Interfaz base que todo provider de precios debe implementar.
    Para agregar una nueva fuente, creá una clase que herede de esta.
    """

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Retorna True si este provider puede manejar la URL dada."""
        pass

    @abstractmethod
    def extract_item_id(self, url: str) -> str:
        """Extrae el identificador único del producto desde la URL."""
        pass

    @abstractmethod
    def get_product_info(self, item_id: str) -> ProductInfo:
        """Consulta el precio y datos del producto. Lanza excepción si falla."""
        pass
