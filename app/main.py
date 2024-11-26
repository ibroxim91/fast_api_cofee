from app import Base, engine, get_db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import User, UserCreate, UserBase
from .models import User as UserModel


app = FastAPI()

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


@app.get("/users/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users does not exist!")
    return users

from fastapi import HTTPException, status

@app.post("/users/", response_model=UserBase)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Foydalanuvchi ismi va emailni tekshirish
    db_user_by_username = db.query(UserModel).filter(UserModel.username == user.username).first()
    db_user_by_email = db.query(UserModel).filter(UserModel.email == user.email).first()

    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Foydalanuvchi yaratish
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserBase(
        username=db_user.username,
        email=db_user.email
    )


