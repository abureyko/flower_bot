# app/models.py
from sqlalchemy import Column, Integer, Float, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    image = Column(String, nullable=False)

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    qty = Column(Integer, default=1)

    product = relationship("Product")