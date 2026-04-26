from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(150))
    description = Column(Text)
    price = Column(DECIMAL(10,2))
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))