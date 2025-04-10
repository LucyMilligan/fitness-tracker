from fastapi import APIRouter
from fastapi import HTTPException
# from sqlmodel import select
from sqlalchemy import select, column

from database.database import SessionDep
from database.models import Activity, User, UserCreate, UserPublic, UserUpdate, OrderBy, SortBy


router = APIRouter()


@router.post("/", response_model=User, status_code=201)
async def create_user(user: UserCreate, session: SessionDep):
    """Endpoint that allows a user to create a user. The user request body
    should be in the format:

        name: str (e.g. "bob")
        email: str (e.g. "bob@gmail.com")
    """
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=list[UserPublic])
async def get_users(session: SessionDep, offset: int = 0, limit: int = 10):
    """Endpoint to get a paginated list of users."""
    users = session.exec(select(User).offset(offset).limit(limit)).scalars().all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
async def get_user_by_user_id(user_id: int, session: SessionDep):
    """Endpoint to get a specific user by user_id. Response does
    not include email address."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserPublic)
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


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    """Endpoint that deletes a user, according to the given user_id.
    If the ID does not exist, an exception with 404 status code is raised."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": f"User_id {user_id} deleted"}


@router.get("/{user_id}/activities/", response_model=list[Activity])
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
