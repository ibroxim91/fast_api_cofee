from sqlalchemy.orm import Session
from app.models import ChatMessage

__all__ = [
    "save_message",
    "get_chat_history",
]

def save_message(db: Session, sender: str, receiver: str, message: str):
    chat_message = ChatMessage(sender=sender, receiver=receiver, message=message)
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message

def get_chat_history(db: Session, user1: str, user2: str):
    return db.query(ChatMessage).filter(
        (ChatMessage.sender == user1) & (ChatMessage.receiver == user2) |
        (ChatMessage.sender == user2) & (ChatMessage.receiver == user1)
    ).order_by(ChatMessage.timestamp).all()
