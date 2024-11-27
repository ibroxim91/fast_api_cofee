from app import Base, engine
from fastapi import FastAPI

from .routes import *

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(category_router, prefix="/category", tags=["category"])

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






