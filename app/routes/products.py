import os
from fastapi import APIRouter, Depends, UploadFile
from app import get_db, crud, schemas
from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.utils.auth_token import get_admin_user, get_current_user
from typing import List, Optional
from fastapi import APIRouter, Depends, Form, File, HTTPException
product_router = APIRouter()


# Product ADD
@product_router.post("/", response_model=schemas.ProductCreate)
def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    image: Optional[UploadFile] = File(None),  # Expecting an UploadFile
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_admin_user)
):
 
    if image:
        file_location = f"static/images/{image.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)  # create directory if not exists
        with open(file_location, "wb") as buffer:
            buffer.write(image.file.read())
    else:
        file_location = None  


    new_product = schemas.ProductCreate(
        name=name,
        description=description,
        price=price,
        category_id=category_id,
        image=file_location  
    )
    return crud.create_product(db=db, product=new_product)


# Products GET
@product_router.get("/", response_model=List[schemas.ProductCreate])
def get_all_products(db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user), skip: int = 0, limit: int = 10):
    return crud.all_products(db=db, skip=skip, limit=limit)


# Product Detail
@product_router.get("/{id}", response_model=schemas.ProductCreate)
def product_detail(id: int, db: Session = Depends(get_db),  current_user: UserModel = Depends(get_current_user)):
    return crud.product_detail(db=db, id=id)


# Product  Update
@product_router.put("/{id}", response_model=schemas.ProductCreate)
def update_product(id: int, product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    return crud.update_product(id, product, db)


# Product Delete
@product_router.delete("/{id}", response_model=dict)
def delete_product(id: int,  db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    return crud.product_delete(id, db)