from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserResponse
from app.repository import users
from app.database import get_db
from app.auth.security import create_access_token, create_refresh_token, get_current_user
from app import schemas, models

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Реєстрація нового користувача
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    created_user = users.create_user(user, db)
    if not created_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return created_user


# Авторизація користувача (вхід) і видача токенів
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users.authenticate_user(user.email, user.password, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(data={"sub": db_user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# Отримання поточного залогіненого користувача
@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user
