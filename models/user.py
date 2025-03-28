from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database.database import Base  # Ensure correct import
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # ✅ Default UUID added
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) 
    avatar_url = Column(String, nullable=False)
    team = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    fantasy_points = relationship("FantasyPoints", back_populates="user", cascade="all, delete")
