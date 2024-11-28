from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.external_service import send_email_to_admins
from app.models import Order, Product, order_products
from fastapi import HTTPException
from sqlalchemy.orm import joinedload


__all__ = [
    "create_order",
    "all_orders",
    "get_order",
    "delete_order",

]

def create_order(db: Session, user: models.User, products: List[schemas.CartAdd]):

    total_price = 0
    db_order = Order(user_id=user.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in products:
        product = db.query(Product).filter(Product.id == item.product).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product} not found")
        total_price += product.price * item.quantity
        association = order_products.insert().values(
            order_id=db_order.id,
            product_id=product.id,
            quantity=item.quantity
        )
        db.execute(association)
 
    db_order.total_price = total_price
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    # Celery Task Send Email 
    # send_email_to_admins.delay(subject="New Order", body="New Order")
    return db_order


def all_orders(db: Session,  user: models.User ):

    orders =  db.query(models.Order).filter(models.Order.user_id == user.id).all()
    if not orders:
        raise HTTPException(status_code=404, detail=f"Orders not found")
    serialized_orders = []
    for order in orders:
        serialized_orders.append({
            "id": order.id,
            "total_price": order.total_price,
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                }
                for product in order.products
            ]
        })
    return serialized_orders


def get_order(db: Session, order_id:int,  user: models.User ):

    order =  db.query(models.Order).filter(models.Order.user_id == user.id, models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order not found")
    serialized_orders = []
    serialized_orders.append({
            "id": order.id,
            "total_price": order.total_price,
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                }
                for product in order.products
            ]
        })
    return serialized_orders


def delete_order(db: Session, order_id:int,  user: models.User ):

    order =  db.query(models.Order).filter(models.Order.user_id == user.id, models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

