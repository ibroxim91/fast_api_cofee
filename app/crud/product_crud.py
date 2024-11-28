import os
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
from app.models import Category as CategoryModel


__all__ = [
    "create_product",
    "product_detail",
    "all_products",
    "update_product",
    "product_delete",
]

def create_product(db: Session, product: schemas.Product):
  
    new_product = models.Product(name=product.name, description=product.description,
                                  price=product.price, category_id=product.category_id, image=product.image
                                  )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def product_detail(id: int, db: Session ):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product does not exist!")
    return product


def all_products(db: Session, skip: int, limit: int ):
    all_products = db.query(models.Product).offset(skip).limit(limit).all()
    if not all_products:
        raise HTTPException(status_code=404, detail="Products does not exist!")
    return all_products


def update_product(id: int, product_update: schemas.ProductCreate, db: Session):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found"
        )


    product.name = product_update.name or product.name
    product.description = product_update.description or product.description
    product.category_id = product_update.category_id or product.category_id
    db.commit()
    db.refresh(product)
    
    return product


def product_delete(id: int, db: Session ):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product does not exist!")
    db.delete(product)
    db.commit()
    return {"message": "product deleted successfully"}
