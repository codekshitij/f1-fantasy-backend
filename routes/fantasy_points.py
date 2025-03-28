from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.fantasy_team import FantasyTeam
from models.fantasy_points import FantasyPoints
from models.user import User
from utils.points_calculator import calculate_fantasy_points
from routes.auth import get_current_user
import uuid

router = APIRouter(prefix="/fantasy/points", tags=["Fantasy Points"])

# ✅ Fetch race results (Mock API or Ergast API)
def get_race_results(race_id: str):
    # Mock race results data (Replace this with real API call)
    return [
        {"driver_id": "max_verstappen", "position": 1, "overtakes": 3, "fastest_lap": True, "constructor": "Red Bull", "points": 25},
        {"driver_id": "lewis_hamilton", "position": 2, "overtakes": 2, "fastest_lap": False, "constructor": "Mercedes", "points": 18},
        {"driver_id": "charles_leclerc", "position": 3, "overtakes": 1, "fastest_lap": False, "constructor": "Ferrari", "points": 15},
        # Add more drivers...
    ]

# ✅ API to Calculate and Store Fantasy Points
@router.post("/{race_id}")
def calculate_fantasy_points_api(race_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Check if the user has a fantasy team
    user_team = db.query(FantasyTeam).filter(FantasyTeam.user_id == user.id).first()
    if not user_team:
        raise HTTPException(status_code=404, detail="Fantasy team not found")

    # Fetch race results (Replace with actual API call)
    race_results = get_race_results(race_id)

    # Calculate fantasy points
    total_points = calculate_fantasy_points(race_results, user_team)

    # Store points in DB
    fantasy_points_entry = FantasyPoints(
        id=str(uuid.uuid4()),
        user_id=user.id,
        race_id=race_id,
        points=total_points
    )
    db.add(fantasy_points_entry)
    db.commit()
    db.refresh(fantasy_points_entry)

    return {"message": "Fantasy points calculated!", "points": total_points}

# ✅ Get User's Fantasy Points
@router.get("/me")
def get_user_fantasy_points(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_points = db.query(FantasyPoints).filter(FantasyPoints.user_id == user.id).all()
    return user_points
