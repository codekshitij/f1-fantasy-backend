import os
import uuid
import requests
from fastapi import APIRouter, HTTPException, Depends, Security
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.database import get_db
from models.user import User
from schemas.user import UserCreate, UserRegister, UserResponse
from dotenv import load_dotenv
from jose import jwt,JWTError
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
import random
import string
import os
import json
from firebase_admin import credentials, initialize_app


  

# Load environment variables
load_dotenv()

# Load SECRET_KEY and ALGORITHM from .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/auth", tags=["Auth"])


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get backend root directory
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "firebase-service-account.json")

# ✅ Initialize Firebase Admin SDK (Only Once)
if not firebase_admin._apps:
    firebase_json = os.getenv("FIREBASE_CREDENTIALS")
    cred = credentials.Certificate(json.loads(firebase_json))
    initialize_app(cred)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Hash Password Function
def hash_password(password: str):
    return pwd_context.hash(password)

# ✅ Verify Password Function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Generate JWT Token
def generate_jwt(email: str):
    return jwt.encode({"email": email}, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ✅ Get Current User from JWT Token
def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Decodes the JWT token and returns the authenticated user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.post("/signup")  # Ensure it's "/signup" in FastAPI
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)  # ✅ Hash before saving

    # ✅ Generate a unique username from email prefix + random 4 characters
    base_username = user.email.split("@")[0]
    
    while True:
        random_suffix = ''.join(random.choices(string.digits, k=4))
        unique_username = f"{base_username}{random_suffix}"
        existing_username = db.query(User).filter(User.username == unique_username).first()
        if not existing_username:
            break  # ✅ Found a unique username

    new_user = User(
        id=uuid.uuid4(),
        name="Temp Name",  
        username=unique_username,  # ✅ Unique username
        email=user.email,
        password=hashed_password,
        avatar_url="default.png",  
        team="None",  
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully!", "access_token": generate_jwt(new_user.email)}


# ✅ 2️⃣ Complete Profile after signup
@router.put("/complete-profile")
def complete_profile(user_data: UserRegister, db: Session = Depends(get_db), token: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.email == token.email).first()  # ✅ Use token.email
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only missing fields
    db_user.name = user_data.name
    db_user.username = user_data.username
    db_user.avatar_url = user_data.avatar_url
    db_user.team = user_data.team

    db.commit()
    db.refresh(db_user)

    return {"message": "Profile completed successfully!"}



# ✅ 3️⃣ Login User (Verify Password)
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful!", "access_token": generate_jwt(db_user.email)}





# ✅ Google Sign-In Route
@router.post("/google-login")
def google_login(token: dict, db: Session = Depends(get_db)):
    google_token = token.get("token")
    if not google_token:
        raise HTTPException(status_code=400, detail="Google token is required")

    try:
        # ✅ Verify the Firebase Token using Admin SDK
        decoded_token = firebase_auth.verify_id_token(google_token)
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        avatar_url = decoded_token.get("picture")

        if not email:
            raise HTTPException(status_code=400, detail="Google authentication failed")

        # ✅ Check if user exists
        existing_user = db.query(User).filter(User.email == email).first()

        if not existing_user:
            # ✅ Create a new user with missing fields
            new_user = User(
                id=uuid.uuid4(),
                name=None,  # 🚨 User must set this in profile modal
                username=email.split("@")[0],
                email=email,
                password="google-auth",
                avatar_url=avatar_url,
                team=None  # 🚨 User must set this in profile modal
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            existing_user = new_user  # Now treat them as an existing user

        # ✅ If user exists but has incomplete profile, return profile setup trigger
        requires_profile_setup = existing_user.name is None or existing_user.team is None

        return {
            "message": "Google Login successful!",
            "access_token": jwt.encode({"email": existing_user.email}, SECRET_KEY, algorithm=ALGORITHM),
            "name": existing_user.name,
            "team": existing_user.team,
            "avatar_url": existing_user.avatar_url,
            "requires_profile_setup": requires_profile_setup
        }

    except Exception as e:
        print("🔥 Firebase Token Verification Failed:", str(e))
        raise HTTPException(status_code=401, detail="Invalid Google token")