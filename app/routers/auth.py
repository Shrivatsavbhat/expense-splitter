from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import UserCreate, Token
from app.core import create_access_token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/auth/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed = pwd_context.hash(user.password)
    db_User = models.User(
        email = user.email,
        hashed_password = hashed
        )
    db.add(db_User)
    db.commit()
    db.refresh(db_User)
    return db_User

@router.post("/auth/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if existing_user is None:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    hashed = existing_user.hashed_password
    verify = pwd_context.verify(form_data.password, hashed)
    if not verify:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = create_access_token(data={"sub": existing_user.email})
    return {"access_token": token, "token_type": "bearer"}

