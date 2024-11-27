import bcrypt
from app import get_db
from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import  UserCreate, UserBase,UserUpdate
from app.models import User as UserModel
from fastapi import HTTPException, status
from app.utils import get_random_verification_code
from app.external_service import SmsSend



def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists by username or email
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

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    db_user = UserModel(
        username=user.username,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password.decode('utf-8'),
        verification_code=get_random_verification_code()  # Generate a random verification code for sms verification
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    SmsSend.send_verification_code_telegram(db_user.phone, db_user.verification_code)
    return UserBase(
        username=db_user.username,
        email=db_user.email
    )


def update_user(id: int, user_update: UserCreate, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.username = user_update.username or user.username
    user.email = user_update.email or user.email
    if user_update.password:
        user.hashed_password = bcrypt.hashpw(user_update.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    db.commit()
    db.refresh(user)
    
    return user


def partial_update(id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_update.username and user_update.username != user.username:
        db_user_by_username = db.query(UserModel).filter(UserModel.username == user_update.username).first()
        if db_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        user.username = user_update.username

    if user_update.email and user_update.email != user.email:
        db_user_by_email = db.query(UserModel).filter(UserModel.email == user_update.email).first()
        if db_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user.email = user_update.email

    if user_update.password:
        user.hashed_password = bcrypt.hashpw(user_update.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    db.commit()
    db.refresh(user)
    
    return user


def delete_user(id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}