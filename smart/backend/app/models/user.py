from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.core.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(20), default="customer")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)