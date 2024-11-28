from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)       
    receiver = Column(String, index=True)  
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  
