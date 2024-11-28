import bcrypt
from fastapi import  Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.utils.auth_token import create_access_token,verify_access_token
from app.models import User as UserModel
from fastapi import HTTPException, Depends
from app import get_db
from sqlalchemy.orm import Session


auth_router = APIRouter()

__all__ = ["auth_router"]

# Зависимость OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

# Схема данных для пользователя
class User(BaseModel):
    username: str
    password: str

# Маршрут для получения токена доступа
@auth_router.post("/access", response_model=Token)
def login_for_access_token(user: User, db: Session = Depends(get_db)):
    user_db = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    if not bcrypt.checkpw(user.password.encode('utf-8'), hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
  

# Маршрут для обновления токена
@auth_router.post("/refresh", response_model=Token)
def refresh_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        username = payload.get("sub")
        new_access_token = create_access_token(data={"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"}

    except HTTPException as e:
        raise e
