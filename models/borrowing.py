from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum


class BorrowStatus(str, enum.Enum):
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"


class BorrowingHistory(Base):
    __tablename__ = "borrowing_history"
    borrow_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    borrow_date = Column(DateTime, nullable=False, default=func.current_timestamp())
    return_date = Column(DateTime)
    status = Column(Enum(BorrowStatus), nullable=False)
