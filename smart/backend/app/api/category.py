from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.category import Category
from pydantic import BaseModel

router = APIRouter()

# request body schema
class CategoryCreate(BaseModel):
    name: str

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ADD CATEGORY
@router.post("/add")
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        new_category = Category(name=category.name)

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return {"message": "Category added", "id": new_category.id}

    except Exception as e:
        db.rollback()
        print("REAL ERROR:", e)   # 👈 THIS LINE
        return {"error": str(e)}

# GET ALL CATEGORIES
@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()