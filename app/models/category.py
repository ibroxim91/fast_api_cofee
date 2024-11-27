from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    products = relationship("Product",  back_populates="category")  

