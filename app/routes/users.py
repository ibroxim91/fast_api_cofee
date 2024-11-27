import bcrypt
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.models import User as UserModel
from app import get_db, crud, schemas
from app.utils import create_access_token
from app.schemas import User,UserUpdate
from app.utils.auth_token import get_admin_user, get_current_user

user_router = APIRouter()

# Foydalanuvchini ro'yxatdan o'tkazish
@user_router.post("/registration")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@user_router.post("/authentication")
def authenticate_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Check user
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Check password
    if not db_user.verify_password(user.password): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # JWT 
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/verification")
def confirm_verification(request: schemas.VerificationRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.phone == request.phone, UserModel.verification_code == request.code).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code or phone number !"
        )
    user.is_active = True
    user.verification_code = None 
    db.commit()
    
    return {"message": "User successfully verified"}


@user_router.get("/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_admin_user) ):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users does not exist!")
    return users


@user_router.post("/me", response_model=User)
def get_me(current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user



@user_router.get("/{id}", response_model=User)
def get_user(id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@user_router.put("/{id}", response_model=User)
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return crud.update_user(id, user_update, db)


@user_router.patch("/{id}", response_model=User)
def partial_update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return crud.partial_update(id, user_update, db)

@user_router.delete("/{id}", response_model=dict)
def delete_user(id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user"
        )
    return crud.delete_user(id, db)   