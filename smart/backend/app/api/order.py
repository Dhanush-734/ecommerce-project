from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.order import Order
from app.models.cart import Cart
from app.models.product import Product
from app.core.security import get_current_user

router = APIRouter()


# =========================
# DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# ✅ CHECKOUT (PROTECTED)
# =========================
@router.post("/checkout")
def checkout(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()

    if not cart_items:
        return {"message": "Cart is empty"}

    total = 0

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        total += product.price * item.quantity

    new_order = Order(
        user_id=current_user.id,
        total_amount=total
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order placed",
        "order_id": new_order.id,
        "total": total
    }


# =========================
# ✅ GET ORDERS (PROTECTED)
# =========================
@router.get("/")
def get_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()