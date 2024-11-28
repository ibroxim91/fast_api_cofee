from fastapi import APIRouter, Depends
from app import get_db, crud, schemas
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.utils.auth_token import get_admin_user, get_current_user
from typing import List

order_router = APIRouter()


#  GET Orders  
@order_router.get("/", response_model=list)
def all_orders( db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.all_orders(db=db, user=current_user)

#  Create Order  
@order_router.post("/", response_model=schemas.OrderBase)
def add_order( cart_products: List[schemas.CartAdd], db: Session = Depends(get_db),   current_user: UserModel = Depends(get_current_user)):
    return crud.create_order(db=db, products=cart_products, user=current_user)


#  GET Order  
@order_router.get("/{id}", response_model=list)
def get_order( id: int, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.get_order(db=db, order_id=id, user=current_user)

#  Delete Order  
@order_router.delete("/{id}", response_model=dict)
def delete_order( id: int, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.delete_order(db=db, order_id=id, user=current_user)