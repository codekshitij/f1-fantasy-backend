from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class RaceResult(BaseModel):
    driver_id: str
    position: int
    overtakes: int
    fastest_lap: bool
    constructor: str
    points: int

class FantasyPointsCreate(BaseModel):
    race_id: str
    points: float

class FantasyPointsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    user_id: str
    race_id: str
    points: float
    created_at: Optional[str]

class LeaderboardEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: str
    username: str
    total_points: float
    team_name: str
    avatar_url: str 