from contextlib import asynccontextmanager
from typing import Annotated
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import select, column, table
import os
from dotenv import load_dotenv

from database import SessionDep, create_db_and_tables
from models import Activity, ActivityCreate, ActivityUpdate, User, UserCreate, UserPublic, UserUpdate, OrderBy, SortBy
from routes import activities

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(activities.router, prefix="/activities")

@app.get("/")
async def get_api_healthcheck():
    return {"message": "API up and running"}

#TODO: add to users.py and change app to router
######################## USERS ENDPOINTS ############################
@app.post("/users/", response_model=User, status_code=201)
async def create_user(user: UserCreate, session: SessionDep):
    """Endpoint that allows a user to create a user"""
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[UserPublic])
async def get_users(session: SessionDep, offset: int = 0, limit: int = 10):
    """Endpoint to get a paginated list of users."""
    users = session.exec(select(User).offset(offset).limit(limit)).scalars().all()
    return users

@app.get("/users/{user_id}", response_model=UserPublic)
async def get_user_by_user_id(user_id: int, session: SessionDep):
    """Endpoint to get a specific user by user_id."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=UserPublic)
async def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    """Endpoint that allows a user of specified user_id to be modified. All
    user properties to be modified are optional, and if no updates occur, the
    original values remain.

    If the user_id does not exist, an exception with 404 status code is raised.
    """
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True) #only includes values sent by the client
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    """Endpoint that deletes a user, according to the given user_id.
    If the ID does not exist, an exception with 404 status code is raised."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": f"User_id {user_id} deleted"}


######################## ACTIVITIES ENDPOINTS ############################
# @app.get("/activities/", response_model=list[Activity])
# async def get_activities(session: SessionDep, offset: int = 0, limit: int = 10, sort_by: SortBy = "id", order_by: OrderBy = "asc"):
#     """Endpoint to get a paginated list of activities.
    
#     :param offset: number of activities to skip
#     :param limit: number of activities to return
#     :param sort_by: column to sort the activities by
#     :param order_by: how to order the activities (ascending or descending)
#     """
#     sort_by_col = column(sort_by)
#     query = select(Activity).offset(offset).limit(limit)

#     if order_by.lower() == "asc":
#         query = query.order_by(sort_by_col.asc())
#     else:
#         query = query.order_by(sort_by_col.desc())

#     activities = session.exec(query).scalars().all()

#     return activities


# @app.get("/users/{user_id}/activities/", response_model=list[Activity])
# async def get_activities_by_user_id(session: SessionDep, user_id: int, offset: int = 0, limit: int = 10, sort_by: SortBy = "id", order_by: OrderBy = "asc"):
#     """Endpoint to get a paginated list of activities.
    
#     :param user_id: user_id for which to get activities for
#     :param offset: number of activities to skip
#     :param limit: number of activities to return
#     :param sort_by: column to sort the activities by
#     :param order_by: how to order the activities (ascending or descending)
#     """
#     sort_by_col = column(sort_by)
#     query = select(Activity).where(Activity.user_id == user_id).offset(offset).limit(limit)

#     if order_by.lower() == "asc":
#         query = query.order_by(sort_by_col.asc())
#     else:
#         query = query.order_by(sort_by_col.desc())

#     activities = session.exec(query).scalars().all()

#     if not activities:
#         raise HTTPException(status_code=404, detail="No activities found")
    
#     return activities


# @app.get("/activities/{id}", response_model=Activity)
# async def get_activity_by_activity_id(id: int, session: SessionDep):
#     """Endpoint that gets a specific activity by id. If the ID does not exist,
#     an exception with 404 status code is raised."""
#     activity = session.get(Activity, id)
#     if not activity:
#         raise HTTPException(status_code=404, detail="Activity not found")
#     return activity


# @app.post("/activities/", response_model=Activity, status_code=201)
# async def create_activity(activity: ActivityCreate, session: SessionDep):
#     """Endpoint that allows a user to create an activity."""
#     db_activity = Activity.model_validate(activity)
#     session.add(db_activity)
#     session.commit()
#     session.refresh(db_activity)
#     return db_activity


# @app.patch("/activities/{id}", response_model=Activity)
# async def update_activity(id: int, activity: ActivityUpdate, session: SessionDep):
#     """Endpoint that allows an activity of specified id to be modified. All
#     activity properties to be modified are optional, and if no updates occur, the
#     original values remain.

#     If the ID does not exist, an exception with 404 status code is raised.
#     """
#     activity_db = session.get(Activity, id)
#     if not activity_db:
#         raise HTTPException(status_code=404, detail="Activity not found")
#     activity_data = activity.model_dump(exclude_unset=True)
#     activity_db.sqlmodel_update(activity_data)
#     session.add(activity_db)
#     session.commit()
#     session.refresh(activity_db)
#     return activity_db


# @app.delete("/activities/{id}")
# async def delete_activity(id: int, session: SessionDep):
#     """Endpoint that deletes an activity, according to the given id.
#     If the ID does not exist, an exception with 404 status code is raised."""
#     activity = session.get(Activity, id)
#     if not activity:
#         raise HTTPException(status_code=404, detail="Activity not found")
#     session.delete(activity)
#     session.commit()
#     return {"message": f"Activity id {id} deleted"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8080)