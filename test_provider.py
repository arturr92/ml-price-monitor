from services.price_service import get_product_info

urls = [
    "https://www.mercadolibre.com.ar/notebook-lenovo-ideapad-1-15amn7-amd-ryzen-5-7520u/p/MLA20656539",
    "https://articulo.mercadolibre.com.ar/MLA-123456789-notebook-ejemplo",
]

for url in urls:
    try:
        info = get_product_info(url)
        print(
            f"✓ {info.item_id} | {info.title[:40]} | ${info.price} {info.currency}")
    except Exception as e:
        print(f"✗ {e}")
