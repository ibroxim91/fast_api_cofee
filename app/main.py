from app import Base, engine
from fastapi import FastAPI
from .routes import *
from app import auth

app = FastAPI()


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(category_router, prefix="/category", tags=["category"])
app.include_router(product_router, prefix="/product", tags=["product"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])
app.include_router(order_router, prefix="/order", tags=["order"])
app.include_router(auth.auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(front_router, prefix="/template", tags=["chat"])

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






