from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    user = relationship("User", back_populates="orders")  
    product = relationship("Product", back_populates="orders") 
