from sqlalchemy.orm import Session
from models.borrowing import BorrowingHistory, BorrowStatus
from models.book import Book
from schemas.borrowing import BorrowingCreate, BorrowingReturn


def borrow_book(db: Session, borrowing: BorrowingCreate):
    db_book = db.query(Book).filter(Book.book_id == borrowing.book_id).first()
    if not db_book:
        raise ValueError("Book not found")
    if db_book.available_copies < 1:
        raise ValueError("No copies available")

    db_book.available_copies -= 1
    db_borrow = BorrowingHistory(
        user_id=borrowing.user_id,
        book_id=borrowing.book_id,
        status=BorrowStatus.BORROWED,
    )
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow


def return_book(db: Session, borrow_id: int, return_data: BorrowingReturn):
    db_borrow = (
        db.query(BorrowingHistory)
        .filter(BorrowingHistory.borrow_id == borrow_id)
        .first()
    )
    if not db_borrow:
        raise ValueError("Borrow record not found")
    if db_borrow.status == BorrowStatus.RETURNED:
        raise ValueError("Book already returned")

    db_book = db.query(Book).filter(Book.book_id == db_borrow.book_id).first()
    if not db_book:
        raise ValueError("Book not found")

    db_borrow.return_date = return_data.return_date
    db_borrow.status = BorrowStatus.RETURNED
    db_book.available_copies += 1
    db.commit()
    db.refresh(db_borrow)
    return db_borrow
