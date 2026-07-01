import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Base de datos
    DATABASE_PATH = os.getenv("DATABASE_PATH", "price_monitor.db")

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("DEBUG", "True") == "True"

    # Email
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

    # Scheduler
    CHECK_INTERVAL_HOURS = int(os.getenv("CHECK_INTERVAL_HOURS", 6))
