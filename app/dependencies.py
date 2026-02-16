from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.crud import get_user_by_email
from app.exceptions import invalid_credentials
from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise invalid_credentials()
    except jwt.PyJWTError:
        raise invalid_credentials()

    user = get_user_by_email(db, email)
    if user is None:
        raise invalid_credentials()
    return user
