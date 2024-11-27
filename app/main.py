from app import Base, engine, get_db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import User, UserCreate, UserBase
from .models import User as UserModel
from fastapi import HTTPException, status
from .routes import *

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")




@app.on_event("startup")
def on_startup():
    init_db()

# Test endpoint
@app.get("/")
def read_test():
    return {"message": "Hello, World!"}






