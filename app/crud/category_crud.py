from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, Depends, status
from app.models import Category as CategoryModel

def create_category(db: Session, category: schemas.CategoryCreate):
    if db.query(models.Category).filter(models.Category.name == category.name).first():
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category {category.name} already exists"
            )
    db_category = models.Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def category_detail(id: int, db: Session ):
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="category does not exist!")
    return category


def all_categories(db: Session, skip: int, limit: int ):
    categories = db.query(CategoryModel).offset(skip).limit(limit).all()
    if not categories:
        raise HTTPException(status_code=404, detail="categories does not exist!")
    return categories


def update_category(id: int, category_update: schemas.CategoryCreate, db: Session):
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="category not found"
        )
    check_name = db.query(CategoryModel).filter(CategoryModel.name == category_update.name).first()

    if check_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
             detail=f"Category {category.name} already exists"
        )

    category.name = category_update.name or category.name
    category.description = category_update.description or category.description
    db.commit()
    db.refresh(category)
    
    return category


def category_delete(id: int, db: Session ):
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="category does not exist!")
    db.delete(category)
    db.commit()
    return {"message": "category deleted successfully"}
