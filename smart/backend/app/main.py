from fastapi import FastAPI

from app.core.database import Base, engine

# ✅ Import models (ONLY ONCE)
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.cart import Cart
from app.models.order_item import OrderItem

# 🚀 Create app
app = FastAPI()

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ Routers
from app.api.user import router as user_router
from app.api.product import router as product_router
from app.api.cart import router as cart_router
from app.api.order import router as order_router
from app.api.category import router as category_router

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(cart_router, prefix="/cart", tags=["Cart"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(category_router, prefix="/categories", tags=["Categories"])

@app.get("/")
def home():
    return {"message": "Working"}