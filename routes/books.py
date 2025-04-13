from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from auth.auth import require_librarian, get_current_user
from crud.book import create_book, update_book, delete_book
from schemas.book import BookCreate, BookUpdate
from models.book import Book
from database import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", dependencies=[Depends(require_librarian)])
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = create_book(db, book)
    if not db_book:
        raise HTTPException(status_code=400, detail="Book creation failed")
    return db_book


@router.put("/{book_id}", dependencies=[Depends(require_librarian)])
def modify_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = update_book(db, book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.delete("/{book_id}", dependencies=[Depends(require_librarian)])
def remove_book(book_id: int, db: Session = Depends(get_db)):
    db_book = delete_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}


@router.get("/", dependencies=[Depends(get_current_user)])
def search_books(
    title: str | None = None,
    author: str | None = None,
    category_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if category_id:
        query = query.filter(Book.category_id == category_id)
    books = query.offset(skip).limit(limit).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books
