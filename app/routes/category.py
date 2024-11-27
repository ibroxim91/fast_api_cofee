from fastapi import APIRouter, Depends
from app import get_db, crud, schemas
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.utils.auth_token import get_admin_user, get_current_user
from typing import List

category_router = APIRouter()


# Category ADD
@category_router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_admin_user)):
    return crud.create_category(db=db, category=category)



# Category GET
@category_router.get("/", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user), skip: int = 0, limit: int = 10):
    return crud.all_categories(db=db, skip=skip, limit=limit)


# Category Detail
@category_router.get("/{id}", response_model=schemas.Category)
def category_detail(id: int, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.category_detail(db=db, id=id)


# Category Update
@category_router.put("/{id}", response_model=schemas.CategoryCreate)
def update_category(id: int, category_update: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    return crud.update_category(id, category_update, db)


# Category Delete
@category_router.delete("/{id}", response_model=dict)
def delete_category(id: int,  db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    return crud.category_delete(id, db)