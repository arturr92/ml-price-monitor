import re


def extract_item_id(url: str) -> str:
    """
    Extrae el item_id de una URL de Mercado Libre.
    Ejemplo: https://www.mercadolibre.com.ar/...-MLA123456789-... → MLA123456789
    """
    if not url or "mercadolibre" not in url.lower():
        raise ValueError(f"URL inválida o no pertenece a Mercado Libre: {url}")

    # Busca el patrón MLA/MLM/MLB + números en la URL
    match = re.search(r'(ML[A-Z])-?(\d+)', url.upper())

    if not match:
        raise ValueError(f"No se encontró un item_id válido en la URL: {url}")

    item_id = match.group(1) + match.group(2)
    return item_id


if __name__ == "__main__":
    # Tests manuales para verificar que funciona
    urls_validas = [
        "https://www.mercadolibre.com.ar/notebook-lenovo-ideapad-1-15amn7-amd-ryzen-5-7520u/p/MLA20656539",
        "https://articulo.mercadolibre.com.ar/MLA-123456789-notebook-ejemplo",
        "https://www.mercadolibre.com.ar/producto?id=MLA987654321&tracking=true"
    ]

    urls_invalidas = [
        "https://www.amazon.com/producto-123",
        "no es una url",
        ""
    ]

    print("=== URLs válidas ===")
    for url in urls_validas:
        try:
            item_id = extract_item_id(url)
            print(f"✓ {item_id} ← {url[:60]}...")
        except ValueError as e:
            print(f"✗ Error: {e}")

    print("\n=== URLs inválidas (deben tirar error) ===")
    for url in urls_invalidas:
        try:
            item_id = extract_item_id(url)
            print(f"✗ No debería llegar acá: {item_id}")
        except ValueError as e:
            print(f"✓ Error esperado: {e}")
