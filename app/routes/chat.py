from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import List
from app.crud import save_message
from app.database import get_db

chat_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Admin  WebSocket
@chat_router.websocket("/ws/chat/admin")
async def admin_chat(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            save_message(db, sender="admin", receiver="user", message=data)
            await manager.broadcast(f"Admin: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# User  WebSocket
@chat_router.websocket("/ws/chat/{username}")
async def user_chat(websocket: WebSocket, username: str, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            save_message(db, sender=username, receiver="admin", message=data)
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)