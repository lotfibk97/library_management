from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    api_key: str
