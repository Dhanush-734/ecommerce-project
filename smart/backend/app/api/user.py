from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

from passlib.context import CryptContext
from app.core.security import create_access_token

import hashlib

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔐 HASH FUNCTION
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= REGISTER =================
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    print("REGISTER API HIT")  # 🔥 debug

    hashed_password = pwd_context.hash(hash_password(user.password))

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# ================= LOGIN =================
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(hash_password(user.password), db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": str(db_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }