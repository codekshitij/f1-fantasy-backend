import os
import uuid
import logging
import traceback
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import get_db
from models.user import User
from schemas.user import UserRegister, UserResponse
from jose import jwt, JWTError
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import auth as firebase_auth
from datetime import datetime

# Load env variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 🔐 Generate JWT token
def generate_jwt(email: str):
    to_encode = {"sub": email}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 🧠 Decode JWT & fetch current user
def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# 🚫 Disabled Signup/Login routes
@router.post("/signup")
def disabled_signup():
    raise HTTPException(status_code=403, detail="Signup is disabled. Use Google login.")

@router.post("/login")
def disabled_login():
    raise HTTPException(status_code=403, detail="Login is disabled. Use Google login.")

# ✅ Google Login
@router.post("/google-login")
def google_login(token: dict, db: Session = Depends(get_db)):
    try:
        if not token or "token" not in token:
            raise HTTPException(status_code=400, detail="Token is required")

        decoded_token = firebase_auth.verify_id_token(token["token"])
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        picture = decoded_token.get("picture")

        if not email:
            raise HTTPException(status_code=400, detail="Email not found in token")

        db_user = db.query(User).filter(User.email == email).first()

        if not db_user:
            db_user = User(
                email=email,
                name=name,
                avatar_url=picture,
                is_active=True,
                is_superuser=False,
                profile_completed=False
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        else:
            db_user.name = name or db_user.name
            db_user.avatar_url = picture or db_user.avatar_url
            db.commit()
            db.refresh(db_user)

        access_token = generate_jwt(email)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.from_orm(db_user)
        }

    except Exception as e:
        logger.error(f"Google login error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

# 🧍‍♂️ Get Current User
@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)
