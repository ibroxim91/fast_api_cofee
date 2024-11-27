from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    phone = Column(String, index=True)
    verification_code = Column(String)
    is_admin = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="owner")  

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, plain_password):
        self.hashed_password = pwd_context.hash(plain_password)