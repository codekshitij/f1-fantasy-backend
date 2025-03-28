import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.user import User
from schemas.user import UserResponse
import os
from dotenv import load_dotenv
from routes.auth import get_current_user  # ✅ Import from `auth.py`

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/users", tags=["Users"])

# ✅ Get Current User Profile (Requires Token)
@router.get("/me", response_model=UserResponse)
def get_user_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns the currently authenticated user.
    """
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        username=current_user.username,
        email=current_user.email,
        avatar_url=current_user.avatar_url,
        team=current_user.team,
        created_at=current_user.created_at.isoformat()  # ✅ Convert datetime to string
    )


# ✅ Get User by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Fetch a user by their ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ✅ Get All Users (For Leaderboard)
@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Returns a list of all users (useful for leaderboards).
    """
    return db.query(User).all()
