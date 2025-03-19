from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

SortBy = Literal[
    "id",
    "user_id",
    "date",
    "time",
    "activity",
    "activity_type",
    "moving_time",
    "distance_km",
    "perceived_effort",
    "elevation_m",
    "date_updated"
]

OrderBy = Literal['ASC', 'DESC', 'asc', 'desc']

class ActivityModel(BaseModel):
    id: int
    user_id: int
    date: str
    time: str
    activity: str
    activity_type: str
    moving_time: str
    distance_km: float
    perceived_effort: int
    elevation_m: int | None = None #optional
    date_updated: datetime = Field(default_factory=datetime.now)

class ActivityUpdateModel(BaseModel):
    user_id: int | None = None
    date: str | None = None
    time: str | None = None
    activity: str | None = None
    activity_type: str | None = None
    moving_time: str | None = None
    distance_km: float | None = None
    perceived_effort: int | None = None
    elevation_m: int | None = None
    date_updated: datetime = Field(default_factory=datetime.now)