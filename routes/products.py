from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import SessionLocal, User
from models.product_repository import create_product
from models.product_repository import validate_user_alert_channel
from services.price_service import get_product_info
import os

products_bp = Blueprint("products", __name__)


@products_bp.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "GET":
        return render_template("add_product.html")

    # POST — procesar el formulario
    db = SessionLocal()
    try:
        name = request.form.get("name", "").strip()
        url = request.form.get("url", "").strip()
        target_price = request.form.get("target_price", "").strip()
        alert_channel = request.form.get("alert_channel", "").strip()

        # Validaciones básicas
        if not all([name, url, target_price, alert_channel]):
            flash("Todos los campos son obligatorios", "danger")
            return render_template("add_product.html")

        try:
            target_price = float(target_price.replace(",", "."))
        except ValueError:
            flash("El precio objetivo debe ser un número válido", "danger")
            return render_template("add_product.html")

        if target_price <= 0:
            flash("El precio objetivo debe ser mayor a cero", "danger")
            return render_template("add_product.html")

        # Obtener o crear usuario por defecto
        user = db.query(User).first()
        if not user:
            user = User(email=os.getenv("SMTP_USER", ""),
                        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""))
            db.add(user)
            db.commit()
            db.refresh(user)

        else:
            # Actualizar datos si faltan
            updated = False
            if not user.email:
                user.email = os.getenv("SMTP_USER", "")
                updated = True
            if not user.telegram_chat_id:
                user.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
                updated = True
            if updated:
                db.commit()
                db.refresh(user)
        # Validar canal de alerta
        try:
            validate_user_alert_channel(db, user.id, alert_channel)
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("add_product.html")

        # Validar URL y obtener precio actual
        try:
            info = get_product_info(url)
        except ValueError as e:
            flash(f"URL inválida: {e}", "danger")
            return render_template("add_product.html")

        # Crear el producto
        create_product(db, user.id, name, url, target_price, alert_channel)
        flash(
            f"✓ Producto '{name}' agregado correctamente. Precio actual: ${info.price:,.0f}", "success")
        return redirect(url_for("dashboard.dashboard"))

    except Exception as e:
        flash(f"Error inesperado: {e}", "danger")
        return render_template("add_product.html")
    finally:
        db.close()
