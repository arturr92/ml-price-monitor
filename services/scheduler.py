from models.product_repository import get_active_products
from models.price_repository import save_price_record
from models.database import SessionLocal
from .price_service import get_product_info
from .logger import setup_logger
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


logger = setup_logger(__name__)

CHECK_INTERVAL_HOURS = int(os.getenv("CHECK_INTERVAL_HOURS", 6))


def run_price_check_cycle():
    """
    Ciclo principal de monitoreo.
    Consulta el precio de todos los productos activos y guarda el historial.
    """
    logger.info(f"{'='*50}")
    logger.info(
        f"Iniciando ciclo de monitoreo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    db = SessionLocal()
    try:
        products = get_active_products(db)
        logger.info(f"Productos activos a monitorear: {len(products)}")

        success_count = 0
        error_count = 0

        for product in products:
            try:
                info = get_product_info(product.url)
                record = save_price_record(db, product.id, info.price)

                if record:
                    logger.info(
                        f"✓ [{product.name}] Precio: ${info.price} — guardado en historial")
                else:
                    logger.info(
                        f"~ [{product.name}] Precio: ${info.price} — sin cambios, no duplicado")

                success_count += 1

            except Exception as e:
                logger.error(
                    f"✗ [{product.name}] Error al consultar precio: {e}")
                error_count += 1
                continue  # El error de un producto no detiene el ciclo

        logger.info(
            f"Ciclo finalizado — Exitosos: {success_count} | Errores: {error_count}")

    finally:
        db.close()


def start_scheduler():
    """
    Inicia el scheduler que corre run_price_check_cycle cada X horas.
    """
    import schedule
    import time

    logger.info(
        f"Scheduler iniciado — intervalo: cada {CHECK_INTERVAL_HOURS} horas")

    # Correr inmediatamente al arrancar
    run_price_check_cycle()

    # Programar el ciclo periódico
    schedule.every(CHECK_INTERVAL_HOURS).hours.do(run_price_check_cycle)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Revisar cada minuto si hay tareas pendientes


if __name__ == "__main__":
    start_scheduler()
