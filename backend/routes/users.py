from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy import select, column

from common.utils import format_query_output, update_activities_dict
from database.database import SessionDep
from database.models import (
    Activity,
    ActivityPlot,
    User,
    UserCreate,
    UserPublic,
    UserUpdate,
    OrderBy,
    SortBy,
)


router = APIRouter()


@router.post("/", response_model=User, status_code=201)
async def create_user(user: UserCreate, session: SessionDep):
    """Endpoint that allows a user to create a user. The user request body
    should be in the format:

        name: str (e.g. "bob")
        email: str (e.g. "bob@gmail.com")

    If any of the fields are in the incorrect format, an exception with 422
    status code is raised.
    """
    try:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except ValueError as e:
        error_messages = [f"{err['loc'][0]} - {err['msg']}" for err in e.errors()]
        raise HTTPException(
            status_code=422,
            detail=f"Format of data incorrect: {", ".join(error_messages)}",
        )


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

    If any of the fields are in the incorrect format, an exception with
    422 status code is raised.
    """
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(
        exclude_unset=True
    )  # only includes values sent by the client
    # model_dump validating against UserUpdate
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
async def get_activities_by_user_id(
    session: SessionDep,
    user_id: int,
    offset: int = 0,
    limit: int = 10,
    sort_by: SortBy = "id",
    order_by: OrderBy = "asc",
):
    """Endpoint to get a paginated list of activities.

    :param user_id: user_id for which to get activities for
    :param offset: number of activities to skip
    :param limit: number of activities to return
    :param sort_by: column to sort the activities by
    :param order_by: how to order the activities (ascending or descending)
    """
    sort_by_col = column(sort_by)
    query = (
        select(Activity).where(Activity.user_id == user_id).offset(offset).limit(limit)
    )

    if order_by.lower() == "asc":
        query = query.order_by(sort_by_col.asc())
    else:
        query = query.order_by(sort_by_col.desc())

    activities = session.exec(query).scalars().all()

    if not activities:
        raise HTTPException(status_code=404, detail="No activities found")

    return activities


@router.get("/{user_id}/activities-to-plot/", response_model=list[ActivityPlot])
async def get_activities_to_plot_by_user_id(
    session: SessionDep,
    user_id: int,
    start_date: str = "1981-01-01",
    end_date: str = "2081-01-01"
):
    """Endpoint to get a list of activity data with added pace, speed and 
    formatted time fields.

    :param user_id: user_id for which to get activities for
    :param start_date: start date for which to get activities after
    :param start_date: end date for which to get activities before
    """
    # explicitly unpacking all columns in the Activiy table (to give a list of tuples
    # instead of ORM objects)
    query = select(*Activity.__table__.c).where(
        Activity.user_id == user_id,
        Activity.date > start_date,
        Activity.date < end_date,
    )
    activities = session.exec(query)
    activities_data = activities.all()
    activities_col_names = activities.keys()

    formatted_activities = format_query_output(activities_data, activities_col_names)
    modified_activities = update_activities_dict(formatted_activities)

    if not modified_activities:
        raise HTTPException(status_code=404, detail="No activities found")

    return modified_activities