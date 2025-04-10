from fastapi import APIRouter, HTTPException
from sqlalchemy import select, column

from database.database import SessionDep
from database.models import Activity, ActivityCreate, ActivityUpdate, OrderBy, SortBy


router = APIRouter()


@router.get("/", response_model=list[Activity])
async def get_activities(
    session: SessionDep,
    offset: int = 0,
    limit: int = 10,
    sort_by: SortBy = "id",
    order_by: OrderBy = "asc",
):
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
    """Endpoint that allows a user to create an activity, with the request body
    validated against the Activity model. The activity request body
    should be in the format:

        user_id: int (e.g. 1)
        date: str, in the format "YYYY/MM/DD" (e.g. "2025/02/24")
        time: str, in the format "hh:mm" (e.g. "17:45")
        activity: str (e.g. "run")
        activity_type: str (e.g. "trail")
        moving_time: str, in the format "hh:mm:ss" (e.g. 00:32:05)
        distance_km: float (e.g. 5.65)
        perceived_effort: int, between 1 (very easy) and 10 (very hard)
        elevation_m: int, optional (e.g. 10)

    If any of the fields are in the incorrect format, an exception with 422
    status code is raised.
    """
    try:
        db_activity = Activity.model_validate(activity)
        session.add(db_activity)
        session.commit()
        session.refresh(db_activity)
        return db_activity
    except ValueError as e:
        error_messages = [f"{err['loc'][0]} - {err['msg']}" for err in e.errors()]
        raise HTTPException(
            status_code=422,
            detail=f"Format of data incorrect: {", ".join(error_messages)}",
        )


@router.patch("/{id}", response_model=Activity)
async def update_activity(id: int, activity: ActivityUpdate, session: SessionDep):
    """Endpoint that allows an activity of specified id to be modified. All
    activity properties to be modified are optional, and if no updates occur, the
    original values remain.

    If the ID does not exist, an exception with 404 status code is raised.

    If any of the fields are in the incorrect format, an exception with
    422 status code is raised.
    """
    activity_db = session.get(Activity, id)
    if not activity_db:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity_data = activity.model_dump(exclude_unset=True)
    # don't need to validate against Activity because model_dump is validating against
    # ActivityUpdate (optional fields required which Activity doesn't have)
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
