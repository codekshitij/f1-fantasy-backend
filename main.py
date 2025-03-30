from fastapi import FastAPI, HTTPException
from database.database import engine, Base, init_db
from routes.user import router as user_router
from routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from routes.fantasy_team import router as fantasy_team_router
from routes.fantasy_points import router as fantasy_points_router
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
import json
import logging
import sys
import os
import traceback
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Initialize Firebase Admin SDK
def init_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate('firebase-credentials.json')
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized successfully")
            return True
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
        logger.error(traceback.format_exc())
        return False

app = FastAPI(title="F1 Fantasy API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
        "https://f1-fantasy-league-dee25.firebaseapp.com",
        "https://f1-fantasy-league-dee25.web.app",
        "https://f1-dream5.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
    max_age=3600
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response

# Initialize Firebase
firebase_initialized = init_firebase()
if not firebase_initialized:
    logger.warning("Firebase initialization failed, some authentication features may not work")

# Initialize database
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Starting application initialization...")
        
        # Initialize database
        logger.info("Starting database initialization...")
        if not init_db():
            logger.error("Database initialization failed")
            raise HTTPException(status_code=500, detail="Database initialization failed")
        
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Unexpected error during application startup: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Application startup failed")

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Test database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "firebase": "initialized" if firebase_initialized else "not initialized"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

# Include routers
try:
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(fantasy_team_router)
    app.include_router(fantasy_points_router)
    logger.info("All routers included successfully")
except Exception as e:
    logger.error(f"Failed to include routers: {e}")
    logger.error(traceback.format_exc())
    raise HTTPException(status_code=500, detail="Failed to initialize application routes")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "F1 Fantasy Backend is running 🚀",
        "version": "1.0.0",
        "status": "online"
    }
