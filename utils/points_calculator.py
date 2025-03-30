from typing import List, Dict
from models.fantasy_team import FantasyTeam

def calculate_position_points(position: int) -> float:
    """Calculate points based on finishing position"""
    points_map = {
        1: 25.0,
        2: 18.0,
        3: 15.0,
        4: 12.0,
        5: 10.0,
        6: 8.0,
        7: 6.0,
        8: 4.0,
        9: 2.0,
        10: 1.0
    }
    return points_map.get(position, 0.0)

def calculate_overtake_points(overtakes: int) -> float:
    """Calculate points for overtakes (2 points per overtake)"""
    return float(overtakes * 2)

def calculate_fastest_lap_points(has_fastest_lap: bool) -> float:
    """Calculate points for fastest lap (1 point)"""
    return 1.0 if has_fastest_lap else 0.0

def calculate_constructor_points(constructor: str, position: int) -> float:
    """Calculate constructor points based on position"""
    base_points = calculate_position_points(position)
    return base_points * 0.5  # Constructor points are worth half of driver points

def calculate_fantasy_points(race_results: List[Dict], user_team: FantasyTeam) -> float:
    """Calculate total fantasy points for a user's team based on race results"""
    total_points = 0.0
    
    # Create a map of driver results for easy lookup
    driver_results = {result["driver_id"]: result for result in race_results}
    
    # Calculate points for each driver in the team
    for driver_id in [user_team.driver_1, user_team.driver_2, user_team.driver_3, user_team.driver_4]:
        if driver_id in driver_results:
            result = driver_results[driver_id]
            driver_points = (
                calculate_position_points(result["position"]) +
                calculate_overtake_points(result["overtakes"]) +
                calculate_fastest_lap_points(result["fastest_lap"])
            )
            total_points += driver_points
    
    # Calculate constructor points
    constructor_results = [r for r in race_results if r["constructor"] == user_team.constructor]
    for result in constructor_results:
        total_points += calculate_constructor_points(result["constructor"], result["position"])
    
    return total_points 