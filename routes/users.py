from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from crud.user import create_user
from schemas.user import UserCreate
from auth.auth import create_jwt_token, pwd_context
from models.user import User
from database import get_db

router = APIRouter(prefix="/users", tags=["users"])


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token(db_user.username)
    return {"access_token": token, "token_type": "bearer"}
