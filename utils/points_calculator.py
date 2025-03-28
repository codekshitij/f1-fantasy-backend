def calculate_fantasy_points(race_results, user_team):
    """
    Calculate fantasy points based on race results and user team selection.

    :param race_results: List of dictionaries containing race results.
    :param user_team: Dictionary containing the user's fantasy team drivers & constructor.
    :return: Total fantasy points.
    """
    points = 0

    for driver in race_results:
        driver_id = driver["driver_id"]
        position = driver["position"]
        overtakes = driver["overtakes"]
        fastest_lap = driver["fastest_lap"]

        # ✅ Check if the driver is in the user's fantasy team
        if driver_id in [user_team.driver_1, user_team.driver_2, user_team.driver_3, user_team.driver_4]:
            # Points for finishing position
            if position == 1:
                points += 25
            elif position == 2:
                points += 18
            elif position == 3:
                points += 15
            elif position <= 10:
                points += 10

            # Points for overtakes
            points += overtakes * 2

            # Points for fastest lap
            if fastest_lap:
                points += 5

            # DNF (Did Not Finish) penalty
            if position == "DNF":
                points -= 5

    # ✅ Constructor Points (Sum of both drivers' race points)
    constructor_points = sum(driver["points"] for driver in race_results if driver["constructor"] == user_team.constructor)
    points += constructor_points

    return points
