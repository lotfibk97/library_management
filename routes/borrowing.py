from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.borrowing import BorrowingHistory
from schemas.borrowing import BorrowingCreate, BorrowingReturn
from crud import borrowing as crud_borrowing
from auth.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/borrowing", tags=["borrowing"])


@router.post("/borrow")
def borrow(
    borrowing: BorrowingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return crud_borrowing.borrow_book(db, borrowing)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/return/{borrow_id}")
def return_book(
    borrow_id: int,
    return_data: BorrowingReturn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        db_borrow = crud_borrowing.return_book(db, borrow_id, return_data)
        return db_borrow
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/history")
def get_borrowing_history(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return (
        db.query(BorrowingHistory)
        .filter(BorrowingHistory.user_id == current_user.user_id)
        .all()
    )
