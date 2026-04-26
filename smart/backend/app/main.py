from fastapi import FastAPI

from app.core.database import Base, engine

# ✅ Import models (ONLY ONCE)
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.cart import Cart
from app.models.order_item import OrderItem
from app.models.category import Category   
from app.models.payment import Payment   # 🔥# 🚀 Create app
app = FastAPI()
from fastapi import FastAPI

app = FastAPI()

try:
    from app.models import user, product, order, cart, order_item, category, payment
    from app.core.database import Base, engine

    Base.metadata.create_all(bind=engine)

    print("✅ DB tables created")

except Exception as e:
    print("❌ ERROR DURING STARTUP:")
    traceback.print_exc()
    raise e
# ✅ Create tables
Base.metadata.create_all(bind=engine)
import traceback
from fastapi import FastAPI

app = FastAPI()

try:
    from app.models import user, product, order, cart, order_item, category, payment
    from app.core.database import Base, engine

    Base.metadata.create_all(bind=engine)

    print("✅ DB tables created")

except Exception as e:
    print("❌ STARTUP ERROR:")
    traceback.print_exc()
    raise e


@app.get("/")
def home():
    return {"message": "Working"}
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