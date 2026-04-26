from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.cart import Cart
from app.schemas.cart import CartCreate
from app.core.security import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ ADD TO CART
@router.post("/add")
def add_to_cart(
    item: CartCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        new_item = Cart(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return {"message": "Item added to cart"}

    except Exception as e:
        db.rollback()
        print("REAL ERROR:", e)   # 👈 IMPORTANT
        return {"error": str(e)}


# ✅ GET CART
@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    return items