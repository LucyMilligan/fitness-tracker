from fastapi import APIRouter
from contextlib import asynccontextmanager
from typing import Annotated
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import select, column, table
import os
from dotenv import load_dotenv

from database import SessionDep
from models import Activity, ActivityCreate, ActivityUpdate, User, UserCreate, UserPublic, UserUpdate, OrderBy, SortBy


router = APIRouter()


@router.get("/users/{user_id}/activities/", response_model=list[Activity])
async def get_activities_by_user_id(session: SessionDep, user_id: int, offset: int = 0, limit: int = 10, sort_by: SortBy = "id", order_by: OrderBy = "asc"):
    """Endpoint to get a paginated list of activities.
    
    :param user_id: user_id for which to get activities for
    :param offset: number of activities to skip
    :param limit: number of activities to return
    :param sort_by: column to sort the activities by
    :param order_by: how to order the activities (ascending or descending)
    """
    sort_by_col = column(sort_by)
    query = select(Activity).where(Activity.user_id == user_id).offset(offset).limit(limit)

    if order_by.lower() == "asc":
        query = query.order_by(sort_by_col.asc())
    else:
        query = query.order_by(sort_by_col.desc())

    activities = session.exec(query).scalars().all()

    if not activities:
        raise HTTPException(status_code=404, detail="No activities found")
    
    return activities
