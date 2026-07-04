import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from .logger import setup_logger

load_dotenv()

logger = setup_logger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


def send_price_alert_email(
    to_email: str,
    product_name: str,
    current_price: float,
    target_price: float,
    product_url: str
) -> bool:
    """
    Envía un email de alerta cuando el precio baja del umbral.
    Retorna True si se envió correctamente, False si falló.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning("Credenciales SMTP no configuradas — email no enviado")
        return False

    subject = f"🔔 Bajó el precio: {product_name}"

    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2E5C8A;">¡Bajó el precio de un producto que estás monitoreando!</h2>
        
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #EAF1F8;">
                <td style="padding: 12px; font-weight: bold;">Producto</td>
                <td style="padding: 12px;">{product_name}</td>
            </tr>
            <tr>
                <td style="padding: 12px; font-weight: bold;">Precio actual</td>
                <td style="padding: 12px; color: #28a745; font-size: 1.2em;">
                    <strong>${current_price:,.2f}</strong>
                </td>
            </tr>
            <tr style="background-color: #EAF1F8;">
                <td style="padding: 12px; font-weight: bold;">Tu precio objetivo</td>
                <td style="padding: 12px;">${target_price:,.2f}</td>
            </tr>
        </table>

        <br>
        <a href="{product_url}" 
           style="background-color: #2E5C8A; color: white; padding: 12px 24px; 
                  text-decoration: none; border-radius: 4px;">
            Ver producto en Mercado Libre
        </a>

        <br><br>
        <p style="color: #888; font-size: 0.8em;">
            Este email fue enviado automáticamente por ML Price Monitor.
        </p>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())

        logger.info(
            f"Email enviado a {to_email} — producto: {product_name} — precio: ${current_price}")
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error(
            "Error de autenticación SMTP — verificá usuario y contraseña de aplicación")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"Error SMTP al enviar email: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al enviar email: {e}")
        return False
