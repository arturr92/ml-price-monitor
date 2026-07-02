from sqlalchemy import (
    create_engine, Column, Integer, String,
    Float, DateTime, Boolean, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
DATABASE_PATH = os.getenv("DATABASE_PATH", "price_monitor.db")
engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "USERS"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=True)
    telegram_chat_id = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    products = relationship(
        "Product", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


class Product(Base):
    __tablename__ = "PRODUCTS"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USERS.id"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    target_price = Column(Float, nullable=False)
    alert_channel = Column(String, nullable=False)  # email / telegram / both
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="products")
    price_history = relationship(
        "PriceHistory", back_populates="product", cascade="all, delete-orphan")
    alerts_sent = relationship(
        "AlertSent", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product id={self.id} name={self.name} target={self.target_price}>"


class PriceHistory(Base):
    __tablename__ = "PRICE_HISTORY"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("PRODUCTS.id"), nullable=False)
    price = Column(Float, nullable=False)
    checked_at = Column(DateTime, default=datetime.now)

    product = relationship("Product", back_populates="price_history")

    def __repr__(self):
        return f"<PriceHistory product_id={self.product_id} price={self.price}>"


class AlertSent(Base):
    __tablename__ = "ALERTS_SENT"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("PRODUCTS.id"), nullable=False)
    price_at_alert = Column(Float, nullable=False)
    channel_used = Column(String, nullable=False)
    sent_at = Column(DateTime, default=datetime.now)

    product = relationship("Product", back_populates="alerts_sent")

    def __repr__(self):
        return f"<AlertSent product_id={self.product_id} channel={self.channel_used}>"


def get_db():
    """Generador de sesiones — usar siempre con context manager."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
