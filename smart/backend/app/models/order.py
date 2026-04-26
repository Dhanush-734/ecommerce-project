from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, default=0)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))