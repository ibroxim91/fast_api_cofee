from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from app.models import Cart


__all__ = [
    "add_cart",
    "delete_product_from_cart",
    "all_cart_products",
    "clear_cart",

]


def all_cart_products(db: Session, user: models.User):
    cart = db.query(Cart).filter(Cart.user_id==user.id).all()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart products does not exist!")
    return cart

def add_cart(db: Session, add_product: schemas.CartAdd, user: models.User):
    product = db.query(models.Product).filter(models.Product.id == add_product.product).first()
    if not product:
        raise HTTPException(status_code=404, detail="product does not exist!")
    
    check_cart = db.query(models.Cart).filter(Cart.user_id==user.id, Cart.product_id==product.id).first()
    if  check_cart:
        if check_cart.quantity != add_product.quantity:
            check_cart.quantity = add_product.quantity
            check_cart.total_price = product.price * add_product.quantity
            db.commit()
            db.refresh(check_cart)
            return check_cart
        else:
            raise HTTPException(status_code=400, detail="You already added this product to your cart!")
  
    total_price = product.price * add_product.quantity
    add_new_product = models.Cart(quantity=add_product.quantity, total_price=total_price,
                                  user_id=user.id, product_id=product.id
                                 
                                  )
    db.add(add_new_product)
    db.commit()
    db.refresh(add_new_product)
    return add_new_product



def delete_product_from_cart(db: Session, product_id: int, user: models.User):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product does not exist!")
    
    check_cart = db.query(models.Cart).filter(Cart.user_id==user.id, Cart.product_id==product_id).first()
    if not check_cart:
        raise HTTPException(status_code=404, detail="This product is not in your cart!")
    
    db.delete(check_cart)
    db.commit()
    return {"message": "Product deleted from cart successfully"}

def clear_cart(db: Session,  user: models.User):
    cart_products = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not cart_products:
        raise HTTPException(status_code=400, detail="Cart is already empty!")
 
    for product in cart_products:
        db.delete(product)
    db.commit()
    return {"message": "Cart cleared successfully"}

