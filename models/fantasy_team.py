from sqlalchemy import Column, String, ForeignKey, Float, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.database import Base

class FantasyTeam(Base):
    __tablename__ = "fantasy_teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    driver_1 = Column(String, nullable=False)
    driver_2 = Column(String, nullable=False)
    driver_3 = Column(String, nullable=False)
    driver_4 = Column(String, nullable=False)
    constructor = Column(String, nullable=False)
    budget_remaining = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
