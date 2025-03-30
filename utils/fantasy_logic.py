
from typing import List, Dict

def calculate_driver_points(driver_result: Dict) -> int:
    points = 0
    pos = driver_result['position']
    grid = driver_result['grid']
    fastest_lap = driver_result.get('fastest_lap', False)

    finish_points = [0, 25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    if 1 <= pos <= 10:
        points += finish_points[pos]

    if fastest_lap:
        points += 1

    pos_change = grid - pos
    points += pos_change

    return points

def calculate_constructor_points(driver_results: List[Dict]) -> int:
    return sum([calculate_driver_points(driver) for driver in driver_results])
