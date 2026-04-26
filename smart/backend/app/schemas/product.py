from pydantic import BaseModel

class ProductCreate(BaseModel):
    product_name: str
    description: str
    price: float
    stock: int
    category_id: int