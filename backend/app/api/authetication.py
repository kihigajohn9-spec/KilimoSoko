from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.data_base import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from app.models.user import User
from app.schemas.authentication import (
    RegisterRequest,
    UserResponse,
    TokenResponse
)
from app.schemas import user


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    if existing_email := db.query(User).filter(
        User.email == user_data.email
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if existing_phone := db.query(User).filter(
        User.phone == user_data.phone
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    hashed_password = hash_password(user_data.password)

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        phone=user_data.phone,
        password=hashed_password,
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    if not (user := db.query(User).filter(
        User.email == login_data.username
    ).first()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        login_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user