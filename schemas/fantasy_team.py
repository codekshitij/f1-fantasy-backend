from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FantasyTeamCreate(BaseModel):
    driver_1: str
    driver_2: str
    driver_3: str
    driver_4: str
    constructor: str
    budget_remaining: float

class FantasyTeamResponse(FantasyTeamCreate):
    id: str  # Ensure ID is a string
    user_id: str  # Ensure user_id is a string
    created_at: Optional[str]  # Convert datetime to string

    class Config:
        from_attributes = True  # ✅ Replaces `orm_mode = True` in Pydantic V2
