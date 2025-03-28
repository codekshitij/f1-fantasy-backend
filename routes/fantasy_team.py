from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.fantasy_team import FantasyTeam
from models.user import User
from schemas.fantasy_team import FantasyTeamCreate, FantasyTeamResponse
from routes.auth import get_current_user
import uuid

router = APIRouter(prefix="/fantasy", tags=["Fantasy Team"])

# ✅ Create a Fantasy Team
@router.get("/team/me", response_model=FantasyTeamResponse)
def get_user_fantasy_team(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    team = db.query(FantasyTeam).filter(FantasyTeam.user_id == user.id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Fantasy team not found")

    # Convert UUIDs and datetime to string
    return {
        "id": str(team.id),
        "user_id": str(team.user_id),
        "driver_1": team.driver_1,
        "driver_2": team.driver_2,
        "driver_3": team.driver_3,
        "driver_4": team.driver_4,
        "constructor": team.constructor,
        "budget_remaining": team.budget_remaining,
        "created_at": team.created_at.isoformat() if team.created_at else None  # Convert datetime to string
    }


# ✅ Get User's Fantasy Team
@router.get("/team/me", response_model=FantasyTeamResponse)
def get_user_fantasy_team(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    team = db.query(FantasyTeam).filter(FantasyTeam.user_id == user.id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Fantasy team not found")
    return team

# ✅ Update Fantasy Team
@router.put("/team/{team_id}")
def update_fantasy_team(team_id: str, team_data: FantasyTeamCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    team = db.query(FantasyTeam).filter(FantasyTeam.id == team_id, FantasyTeam.user_id == user.id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Fantasy team not found")

    team.driver_1 = team_data.driver_1
    team.driver_2 = team_data.driver_2
    team.driver_3 = team_data.driver_3
    team.driver_4 = team_data.driver_4
    team.constructor = team_data.constructor
    team.budget_remaining = team_data.budget_remaining

    db.commit()
    db.refresh(team)
    return {"message": "Fantasy team updated successfully"}

# ✅ Delete Fantasy Team
@router.delete("/team/{team_id}")
def delete_fantasy_team(team_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    team = db.query(FantasyTeam).filter(FantasyTeam.id == team_id, FantasyTeam.user_id == user.id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Fantasy team not found")

    db.delete(team)
    db.commit()
    return {"message": "Fantasy team deleted successfully"}
