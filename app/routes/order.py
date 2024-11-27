from fastapi import APIRouter, Depends
from app import get_db, crud, schemas
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.utils.auth_token import get_admin_user, get_current_user
from typing import List

order_router = APIRouter()


#  GET Orders  
@order_router.get("/", response_model=List[schemas.Cart])
def add_product( db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.all_cart_products(db=db, user=current_user)
