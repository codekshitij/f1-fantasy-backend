# /app/utils/team_validation.py
from typing import List, Dict
from data.prices import DRIVER_PRICES, CONSTRUCTOR_PRICES

MAX_BUDGET = 45_000_000

def calculate_team_cost(drivers: List[str], constructor: str) -> int:
    total = sum(DRIVER_PRICES.get(driver, 0) for driver in drivers)
    total += CONSTRUCTOR_PRICES.get(constructor, 0)
    return total

def is_valid_team(drivers: List[str], constructor: str) -> Dict:
    if len(drivers) != 5:
        return {"valid": False, "reason": "Team must have exactly 5 drivers."}
    
    if constructor not in CONSTRUCTOR_PRICES:
        return {"valid": False, "reason": "Invalid constructor selected."}
    
    cost = calculate_team_cost(drivers, constructor)
    
    if cost > MAX_BUDGET:
        return {"valid": False, "reason": f"Team cost exceeds budget. Cost: {cost}, Budget: {MAX_BUDGET}"}
    
    return {"valid": True, "total_cost": cost}
