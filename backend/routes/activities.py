from fastapi import APIRouter
from contextlib import asynccontextmanager
from typing import Annotated
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import select, column, table
import os
from dotenv import load_dotenv

from database import SessionDep
from models import Activity, ActivityCreate, ActivityUpdate, User, UserCreate, UserPublic, UserUpdate, OrderBy, SortBy


router = APIRouter()

@router.get("/", response_model=list[Activity])
async def get_activities(session: SessionDep, offset: int = 0, limit: int = 10, sort_by: SortBy = "id", order_by: OrderBy = "asc"):
    """Endpoint to get a paginated list of activities.
    
    :param offset: number of activities to skip
    :param limit: number of activities to return
    :param sort_by: column to sort the activities by
    :param order_by: how to order the activities (ascending or descending)
    """
    sort_by_col = column(sort_by)
    query = select(Activity).offset(offset).limit(limit)

    if order_by.lower() == "asc":
        query = query.order_by(sort_by_col.asc())
    else:
        query = query.order_by(sort_by_col.desc())

    activities = session.exec(query).scalars().all()

    return activities


@router.get("/{id}", response_model=Activity)
async def get_activity_by_activity_id(id: int, session: SessionDep):
    """Endpoint that gets a specific activity by id. If the ID does not exist,
    an exception with 404 status code is raised."""
    activity = session.get(Activity, id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/", response_model=Activity, status_code=201)
async def create_activity(activity: ActivityCreate, session: SessionDep):
    """Endpoint that allows a user to create an activity."""
    db_activity = Activity.model_validate(activity)
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return db_activity


@router.patch("/{id}", response_model=Activity)
async def update_activity(id: int, activity: ActivityUpdate, session: SessionDep):
    """Endpoint that allows an activity of specified id to be modified. All
    activity properties to be modified are optional, and if no updates occur, the
    original values remain.

    If the ID does not exist, an exception with 404 status code is raised.
    """
    activity_db = session.get(Activity, id)
    if not activity_db:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity_data = activity.model_dump(exclude_unset=True)
    activity_db.sqlmodel_update(activity_data)
    session.add(activity_db)
    session.commit()
    session.refresh(activity_db)
    return activity_db


@router.delete("/{id}")
async def delete_activity(id: int, session: SessionDep):
    """Endpoint that deletes an activity, according to the given id.
    If the ID does not exist, an exception with 404 status code is raised."""
    activity = session.get(Activity, id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    session.delete(activity)
    session.commit()
    return {"message": f"Activity id {id} deleted"}