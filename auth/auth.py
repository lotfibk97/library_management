from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "test-secret-key")
ALGORITHM = "HS256"


async def get_current_user(
    api_key: str = Header(..., alias="api-key"), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user


async def get_current_user_jwt(token: str = Header(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def require_librarian(user=Depends(get_current_user)):
    if user.role != "LIBRARIAN":
        raise HTTPException(status_code=403, detail="Librarian access required")
    return user


def create_jwt_token(username: str):
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"sub": username, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
