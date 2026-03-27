from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
