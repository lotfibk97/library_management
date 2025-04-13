from pydantic import BaseModel
from datetime import datetime


class BorrowingCreate(BaseModel):
    user_id: int
    book_id: int


class BorrowingReturn(BaseModel):
    return_date: str
