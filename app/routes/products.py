from fastapi import APIRouter, Depends
from app import get_db, crud, schemas
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.utils.auth_token import get_admin_user, get_current_user
from typing import List

product_router = APIRouter()


# Product ADD
@product_router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_admin_user)):
    return crud.create_product(db=db, product=product)



# Products GET
@product_router.get("/", response_model=List[schemas.Product])
def get_all_products(db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user), skip: int = 0, limit: int = 10):
    return crud.all_products(db=db, skip=skip, limit=limit)


# Product Detail
@product_router.get("/{id}", response_model=schemas.Product)
def category_detail(id: int, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.product_detail(db=db, id=id)


# Product  Update
@product_router.put("/{id}", response_model=schemas.Product)
def update_product(id: int, product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    return crud.update_product(id, product, db)


# Product Delete
@product_router.delete("/{id}", response_model=dict)
def delete_category(id: int,  db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    return crud.product_delete(id, db)