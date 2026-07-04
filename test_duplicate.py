from models.alert_repository import should_send_alert, register_alert_sent
from models.product_repository import create_product
from models.database import SessionLocal, Base, engine, User, Product, PriceHistory, AlertSent
from dotenv import load_dotenv
load_dotenv()


Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Limpiar datos anteriores
db.query(AlertSent).delete()
db.query(PriceHistory).delete()
db.query(Product).delete()
db.query(User).delete()
db.commit()

# Setup
user = User(email="arturo@test.com")
db.add(user)
db.commit()
db.refresh(user)

product = create_product(
    db, user.id, "Notebook Lenovo",
    "https://articulo.mercadolibre.com.ar/MLA-123456789-notebook",
    140000.0, "both"
)

print("=== Test should_send_alert ===\n")

# Precio por encima del umbral — no debe alertar
result = should_send_alert(db, product.id, 150000.0, 140000.0)
print(f"✓ Precio sobre umbral (150k > 140k) → debe ser False: {result}")

# Primera vez bajo el umbral — debe alertar
result = should_send_alert(db, product.id, 138000.0, 140000.0)
print(f"✓ Primera baja (138k ≤ 140k) → debe ser True: {result}")

# Registrar la alerta
register_alert_sent(db, product.id, 138000.0, "both")
print(f"✓ Alerta registrada a $138,000")

# Mismo precio — no debe alertar de nuevo
result = should_send_alert(db, product.id, 138000.0, 140000.0)
print(f"✓ Mismo precio (138k) → debe ser False: {result}")

# Precio bajó aún más — debe alertar de nuevo
result = should_send_alert(db, product.id, 135000.0, 140000.0)
print(f"✓ Nueva baja (135k < 138k) → debe ser True: {result}")

# Registrar segunda alerta
register_alert_sent(db, product.id, 135000.0, "both")
print(f"✓ Segunda alerta registrada a $135,000")

# Precio subió y volvió al mismo nivel — no debe alertar
result = should_send_alert(db, product.id, 135000.0, 140000.0)
print(f"✓ Mismo precio que última alerta (135k) → debe ser False: {result}")

db.close()
