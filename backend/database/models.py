from datetime import datetime
from typing import Literal
from pydantic import BaseModel, field_validator
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
    "date_updated",
]

OrderBy = Literal["ASC", "DESC", "asc", "desc"]


class UserBase(SQLModel):
    name: str


class User(UserBase, table=True):
    __tablename__ = "user_table"
    user_id: int | None = Field(default=None, primary_key=True)
    email: str

    @field_validator("email", mode="before")
    @classmethod
    def date_valid(cls, value: str):
        if "@" not in value:
            raise ValueError("Invalid email address.")
        return value


class UserPublic(UserBase):
    user_id: int
    # email stays hidden for public users


class UserCreate(UserBase):
    # user_id auto generated
    email: str


class UserUpdate(UserBase):
    # optional updates to a specific user_id
    name: str | None = None
    email: str | None = None

    @field_validator("email", mode="before")
    @classmethod
    def date_valid(cls, value: str):
        if "@" not in value:
            raise ValueError("Invalid email address.")
        return value


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

    @field_validator("date", mode="before")
    @classmethod
    def date_valid(cls, value: str):
        try:
            datetime.strptime(value, "%Y/%m/%d")
            return value
        except (ValueError, TypeError):
            raise ValueError("Date does not match format 'YYYY/MM/DD'")

    @field_validator("time", mode="before")
    @classmethod
    def time_valid(cls, value: str):
        try:
            datetime.strptime(value, "%H:%M")
            return value
        except (ValueError, TypeError):
            raise ValueError("Time does not match format 'HH:MM'")

    @field_validator("moving_time", mode="before")
    @classmethod
    def moving_time_valid(cls, value: str):
        try:
            hours, minutes, seconds = map(int, value.split(":"))
            return value
        except (ValueError, AttributeError):
            raise ValueError("Time does not match format 'HH:MM:SS'")

    @field_validator("activity", mode="before")
    @classmethod
    def activity_valid(cls, value: str):
        valid_activities = ["run", "ride"]
        if value not in valid_activities:
            raise ValueError(f"Activity not in {valid_activities}")
        return value

    @field_validator("perceived_effort", mode="before")
    @classmethod
    def perceived_effort_valid(cls, value: int):
        try:
            if value < 1 or value > 10:
                raise ValueError("Perceived_effort not in range 1 - 10")
            return value
        except TypeError:
            raise ValueError("Perceived_effort not a valid number in the range 1 - 10")


class ActivityCreate(SQLModel):
    # id auto generated
    user_id: int
    date: str
    time: str
    activity: str
    activity_type: str
    moving_time: str
    distance_km: float
    perceived_effort: int
    elevation_m: int | None = None


class ActivityUpdate(SQLModel):  # optional updates to a specific activity id
    user_id: int | None = None
    date: str | None = None
    time: str | None = None
    activity: str | None = None
    activity_type: str | None = None
    moving_time: str | None = None
    distance_km: float | None = None
    perceived_effort: int | None = None
    elevation_m: int | None = None

    @field_validator("date", mode="before")
    @classmethod
    def date_valid(cls, value: str):
        try:
            datetime.strptime(value, "%Y/%m/%d")
            return value
        except (ValueError, TypeError):
            raise ValueError("Date does not match format 'YYYY/MM/DD'")

    @field_validator("time", mode="before")
    @classmethod
    def time_valid(cls, value: str):
        try:
            datetime.strptime(value, "%H:%M")
            return value
        except (ValueError, TypeError):
            raise ValueError("Time does not match format 'HH:MM'")

    @field_validator("moving_time", mode="before")
    @classmethod
    def moving_time_valid(cls, value: str):
        try:
            hours, minutes, seconds = map(int, value.split(":"))
            return value
        except (ValueError, AttributeError):
            raise ValueError("Time does not match format 'HH:MM:SS'")

    @field_validator("activity", mode="before")
    @classmethod
    def activity_valid(cls, value: str):
        valid_activities = ["run", "ride"]
        if value not in valid_activities:
            raise ValueError(f"Activity not in {valid_activities}")
        return value

    @field_validator("perceived_effort", mode="before")
    @classmethod
    def perceived_effort_valid(cls, value: int):
        try:
            if value < 1 or value > 10:
                raise ValueError("Perceived_effort not in range 1 - 10")
            return value
        except TypeError:
            raise ValueError("Perceived_effort not a valid number in the range 1 - 10")


#unsure if this is needed, but added for consistency (response_model for endpoint)
class ActivityPlot(BaseModel):
    id: int
    user_id: int
    date: str
    time: str
    activity: str
    activity_type: str
    moving_time: str
    distance_km: float
    perceived_effort: int
    elevation_m: int
    pace_str_mps: str
    pace_float_mps: float
    speed_kmphr: float
    formatted_time: str