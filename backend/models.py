"""
SQLAlchemy ORM models for FinPilot AI.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class Transaction(Base):
    """Transaction model: income or expense with category and description."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String(20), nullable=False)  # 'income' or 'expense'
    description = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
