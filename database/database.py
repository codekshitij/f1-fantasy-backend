# Import required libraries from SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the .env file
env_path = Path(__file__).parent.parent / '.env'

# Load environment variables
load_dotenv(dotenv_path=env_path)

# Database URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

logger.info(f"Connecting to database...")

# Create Engine with SSL mode for Neon
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=60,  # Increased timeout
    connect_args={
        "sslmode": "require",
        "connect_timeout": 60,  # Increased connection timeout
        "keepalives": 1,  # Enable keepalive
        "keepalives_idle": 30,  # Keepalive idle time
        "keepalives_interval": 10,  # Keepalive interval
        "keepalives_count": 5  # Number of keepalive attempts
    },
    echo=True  # Enable SQL logging for debugging
)

# Session Local with increased timeout
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=False  # Prevent expired object issues
)

# Base Declaration
Base = declarative_base()

def test_connection():
    """Test database connection with retries"""
    max_retries = 5  # Increased retries
    retry_delay = 5  # Increased delay
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Testing database connection (attempt {attempt + 1}/{max_retries})...")
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                result.fetchone()  # Actually fetch the result
                logger.info("Database connection successful!")
                return True
        except Exception as e:
            logger.error(f"Connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Failed to connect to database after all retries")
                return False

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    try:
        logger.info(f"Checking if table {table_name} exists...")
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')"))
            exists = result.scalar()
            logger.info(f"Table {table_name} exists: {exists}")
            return exists
    except Exception as e:
        logger.error(f"Error checking table existence: {e}")
        return False

def create_tables():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False

# Function to make team column nullable
def make_team_nullable():
    try:
        if not check_table_exists('users'):
            logger.info("Users table does not exist yet, skipping team column modification")
            return
            
        with engine.connect() as connection:
            connection.execute(text("ALTER TABLE users ALTER COLUMN team DROP NOT NULL;"))
            connection.commit()
            logger.info("Successfully made team column nullable")
    except Exception as e:
        logger.error(f"Error making team nullable: {e}")
        # Don't raise the error, as this is not critical

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    try:
        # Test connection first
        if not test_connection():
            logger.error("Could not establish database connection")
            return False
            
        # Create tables
        if not create_tables():
            logger.error("Failed to create database tables")
            return False
            
        # Make team nullable after tables are created
        make_team_nullable()
        
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False
