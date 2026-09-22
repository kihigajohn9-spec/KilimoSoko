from datetime import datetime, timedelta, timezone

from jose import jwt,JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.core.config import settings
from app.models.user import User
from sqlalchemy.orm import Session
from app.core.data_base import get_db



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/auth/login"
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

#password hashing and verification functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


#JWT token creation function
def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode["exp"] = expire

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError as error:
        raise credentials_exception from error

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise credentials_exception

    return user