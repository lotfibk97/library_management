from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    category_id: int
    isbn: str
    total_copies: int
    available_copies: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    category_id: int | None = None
    isbn: str | None = None
    total_copies: int | None = None
    available_copies: int | None = None
