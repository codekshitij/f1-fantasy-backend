from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database.database import Base  # Ensure correct import
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # ✅ Default UUID added
    name = Column(String, nullable=True)  # Made nullable for Google login
    username = Column(String, unique=True, nullable=True)  # Made nullable for Google login
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Made nullable for Google login
    avatar_url = Column(String, nullable=True)  # Made nullable for Google login
    team = Column(String, nullable=True)  # Allow team to be set later
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    profile_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    fantasy_points = relationship("FantasyPoints", back_populates="user", cascade="all, delete")
