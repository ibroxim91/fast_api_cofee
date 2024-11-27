from fastapi import APIRouter, Depends
from app import get_db, crud, schemas
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.utils.auth_token import get_admin_user, get_current_user
from typing import List

cart_router = APIRouter()


#  ADD Product  
@cart_router.get("/", response_model=List[schemas.Cart])
def add_product( db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.all_cart_products(db=db, user=current_user)


#  ADD Product  
@cart_router.post("/", response_model=schemas.Cart)
def add_product(new_product: schemas.CartAdd, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.add_cart(db=db, add_product=new_product, user=current_user)


#  Delete  Product  
@cart_router.delete("/{id}", response_model=dict)
def delete_product(id: int, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.delete_product_from_cart(db=db, product_id=id, user=current_user)


#  Clear Cart  
@cart_router.delete("/", response_model=dict)
def delete_product( db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.clear_cart(db=db, user=current_user)
