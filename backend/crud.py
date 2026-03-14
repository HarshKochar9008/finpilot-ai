"""
CRUD operations for transactions. Used by FastAPI routes.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models import Transaction
from backend.schemas import TransactionCreate


def create_transaction(db: Session, transaction: TransactionCreate) -> Transaction:
    """Insert a new transaction and return it."""
    db_transaction = Transaction(
        category=transaction.category,
        amount=transaction.amount,
        type=transaction.type,
        description=transaction.description or "",
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(db: Session) -> list[Transaction]:
    """Return all transactions, newest first."""
    return db.query(Transaction).order_by(Transaction.created_at.desc()).all()


def get_summary(db: Session) -> dict[str, float]:
    """
    Return total_income, total_expenses, and balance.
    Income and expenses are summed by type.
    """
    income = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(Transaction.type == "income")
        .scalar()
        or 0
    )
    expenses = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(Transaction.type == "expense")
        .scalar()
        or 0
    )
    return {
        "total_income": float(income),
        "total_expenses": float(expenses),
        "balance": float(income - expenses),
    }
