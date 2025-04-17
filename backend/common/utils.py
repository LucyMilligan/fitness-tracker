from typing import Any, Dict, List
from copy import deepcopy


def calculate_time_secs(moving_time: str) -> int:
    """calculates the moving time in seconds, given an input moving_time in the format
    "HH:MM:SS. Returns the time in secs as an integer."
    """
    hours, minutes, seconds = map(int, moving_time.split(":"))
    time_secs = seconds + (minutes * 60) + (hours * 60 * 60)
    return time_secs


def calculate_pace_mins_per_km(distance: float, moving_time: str) -> str:
    """Calculates the pace of an activity in minutes per km, returning the pace as
    a string in the format "MM:SS"
    """
    time_secs = calculate_time_secs(moving_time)
    pace_secs_per_km = time_secs / distance
    pace_mins = int(pace_secs_per_km // 60)
    pace_secs = int(pace_secs_per_km % 60)
    return f"{pace_mins}:{str(pace_secs).rjust(2, "0")}"


def calculate_speed_km_per_hr(distance: float, moving_time: str) -> float:
    time_secs = calculate_time_secs(moving_time)
    time_hrs = time_secs / (60 * 60)
    speed = distance / time_hrs
    return round(speed, 2)


def convert_pace_to_float(pace_string: str) -> float:
    """takes a pace string in the format "MM:SS" (min/km) and converts it into a float.
    e.g. "6:53" would return 6.88 min/km. This is for ease of plotting the data."""
    minutes, seconds = map(int, pace_string.split(":"))
    return round((minutes + (seconds / 60)), 2)


def convert_date_to_dt_format(date: str) -> str:
    """converts date string (original format "YYYY/MM/DD") into ISO 8601 format"""
    year, month, day = date.split("/")
    formatted_date_str = f"{year}-{month}-{day}T00:00:00.000Z"
    return formatted_date_str


def update_activities_dict(activities_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """updates the activities data returned from the API with additional keys of pace_str_mps,
    pace_float_mps, speed_kmphr and formatted_time"""
    updated_activities = deepcopy(activities_data)
    for activity in updated_activities:
        distance = activity["distance_km"]
        moving_time = activity["moving_time"]
        date = activity["date"]
        activity["pace_str_mps"] = calculate_pace_mins_per_km(distance, moving_time)
        activity["pace_float_mps"] = convert_pace_to_float(activity["pace_str_mps"])
        activity["speed_kmphr"] = calculate_speed_km_per_hr(distance, moving_time)
        activity["formatted_time"] = convert_date_to_dt_format(date)
    return updated_activities