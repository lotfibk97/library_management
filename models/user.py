from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum


class UserRole(str, enum.Enum):
    USER = "USER"
    LIBRARIAN = "LIBRARIAN"


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    api_key = Column(String, unique=True, nullable=False)
