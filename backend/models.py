from datetime import datetime
from typing import Literal
from sqlmodel import Field, SQLModel

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


class UserBase(SQLModel):
    name: str


class User(UserBase, table=True):
    __tablename__ = "user_table"
    user_id: int | None = Field(default=None, primary_key=True)
    email: str


class UserPublic(UserBase):
    user_id: int
    #email stays hidden for public users


class UserCreate(UserBase):
    #user_id auto generated
    email: str


class UserUpdate(UserBase): 
    #optional updates to a specific user_id
    name: str | None = None
    email: str | None = None


class Activity(SQLModel, table=True):
    __tablename__ = "activity_table"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_table.user_id")
    date: str
    time: str
    activity: str
    activity_type: str
    moving_time: str
    distance_km: float
    perceived_effort: int
    elevation_m: int | None = None


class ActivityCreate(SQLModel):
    #id auto generated
    user_id: int
    date: str
    time: str
    activity: str
    activity_type: str
    moving_time: str
    distance_km: float
    perceived_effort: int
    elevation_m: int | None = None


class ActivityUpdate(SQLModel): 
    #optional updates to a specific activity id
    user_id: int | None = None
    date: str | None = None
    time: str | None = None
    activity: str | None = None
    activity_type: str | None = None
    moving_time: str | None = None
    distance_km: float | None = None
    perceived_effort: int | None = None
    elevation_m: int | None = None