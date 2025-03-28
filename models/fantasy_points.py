from sqlalchemy import Column, ForeignKey, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database.database import Base
from sqlalchemy.sql import func


class FantasyPoints(Base):
    __tablename__ = "fantasy_points"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    race_id = Column(String, nullable=False)  # Unique identifier for the race
    points = Column(Float, nullable=False, default=0.0)
    created_at = Column(String, default=func.now())

    user = relationship("User", back_populates="fantasy_points")
