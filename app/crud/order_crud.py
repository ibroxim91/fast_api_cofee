from sqlalchemy.orm import Session
from typing import List
from app.models import Order, Product
from fastapi import HTTPException, status

__all__ = [
    "create_order"
]

def create_order(db: Session, user_id: int, products: List[dict]):

    total_price = 0

    # Buyurtma yaratish
    db_order = Order(user_id=user_id)

    for item in products:
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item['product_id']} not found")
        total_price += product.price * item["quantity"]

        # Yordamchi jadval orqali bog‘lash
        db_order.products.append(product)

    db_order.total_price = total_price
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
