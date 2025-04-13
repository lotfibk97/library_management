from sqlalchemy.orm import Session
from models.user import User, UserRole
from schemas.user import UserCreate
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    api_key = str(uuid.uuid4())
    db_user = User(
        username=user.username,
        password_hash=hashed_password,
        role=UserRole[user.role],
        api_key=api_key,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
