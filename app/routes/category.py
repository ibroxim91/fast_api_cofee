from fastapi import APIRouter, HTTPException, Depends, status
from app import get_db, crud, schemas
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.utils.auth_token import get_admin_user, get_current_user

category_router = APIRouter()


@category_router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_admin_user)):
    db_category = crud.create_category(db=db, category=category)
    return db_category