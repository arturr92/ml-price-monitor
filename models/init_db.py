from database import Base, engine, User, Product, PriceHistory, AlertSent


def init_db():
    """Crea todas las tablas si no existen. Es idempotente — se puede correr múltiples veces."""
    print("Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas correctamente:")
    for table in Base.metadata.tables.keys():
        print(f"  - {table}")


if __name__ == "__main__":
    init_db()
