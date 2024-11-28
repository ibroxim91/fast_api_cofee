from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import Base
from .order import order_products


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    image = Column(String, nullable=True)
    category = relationship("Category", back_populates="products")  
    orders = relationship(
        "Order",
        secondary=order_products,
        back_populates="products"
    )