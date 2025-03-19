import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from models import ActivityModel, ActivityUpdateModel, OrderBy, SortBy

app = FastAPI()

activities = [
    {
        "id": 1,
        "user_id": 1,
        "date": "2025-03-18",
        "time": "11:18",
        "activity": "run",
        "activity_type": "trail",
        "moving_time": "00:30:35",
        "distance_km": 5.5,
        "perceived_effort": 5,
        "elevation_m": 25,
        "date_updated": "2025-03-18T19:00:00.000"
    },
    {
        "id": 2,
        "user_id": 1,
        "date": "2025-03-17",
        "time": "17:45",
        "activity": "run",
        "activity_type": "trail",
        "moving_time": "01:15:00",
        "distance_km": 10,
        "perceived_effort": 2,
        "elevation_m": 140,
        "date_updated": "2025-03-17T18:00:00.000"
    }
]

@app.get("/")
async def get_api_healthcheck():
    return {"message": "API up and running"}


@app.get("/activities")
async def get_activities(skip: int = 0, limit: int = 10, sort_by: SortBy = "id", order_by: OrderBy = "asc"):
    """endpoint to get a paginated list of activities.

    :param skip: number of activities to skip
    :param limit: number of activities to return
    """
    if order_by.lower() == "asc":
        activities_sorted = sorted(activities, key=lambda x: x[sort_by])
    else:
        activities_sorted = sorted(activities, key=lambda x: x[sort_by], reverse=True)
    return activities_sorted[skip:skip+limit]


@app.get("/activities/{id}")
async def get_activity_by_id(id: int):
    """endpoint that gets activities by id. If the ID does not exist,
    an exception with 404 status code is raised."""
    for activity in activities:
        if activity["id"] == int(id):
            return activity

    raise HTTPException(
        status_code=404,
        detail=f"activity with id of {id} does not exist"
    )


@app.get("/users/{user_id}/activities")
async def get_activity_by_user_id(user_id: int):
    """endpoint that gets activities by user_id."""
    user_activities = []
    for activity in activities:
        if activity["user_id"] == int(user_id):
            user_activities.append(activity)

    if user_activities:
        return user_activities

    raise HTTPException(
        status_code=404,
        detail=f"no activities recorded for user_id {user_id}"
    )


@app.post("/activities", status_code=201)
async def create_activity(activity: ActivityModel):
    """endpoint that allows a user to create an activity."""
    activities.append(activity.model_dump())
    return activity


@app.patch("/activities/{id}")
async def update_activity(id: int, updated_activity: ActivityUpdateModel):
    """endpoint that allows an activity of specified id to be modified. All
    activity properties to be modified are optional, and if no updates occur, the
    original values remain.

    If the ID does not exist, an exception with 404 status code is raised.
    """
    for activity in activities:
        if activity["id"] == int(id):
            activity["user_id"] = updated_activity.user_id if updated_activity.user_id else activity["user_id"]
            activity["date"] = updated_activity.date if updated_activity.date else activity["date"]
            activity["time"] = updated_activity.time if updated_activity.time else activity["time"]
            activity["activity"] = updated_activity.activity if updated_activity.activity else activity["activity"]
            activity["activity_type"] = updated_activity.activity_type if updated_activity.activity_type else activity["activity_type"]
            activity["moving_time"] = updated_activity.moving_time if updated_activity.moving_time else activity["moving_time"]
            activity["distance_km"] = updated_activity.distance_km if updated_activity.distance_km else activity["distance_km"]
            activity["perceived_effort"] = updated_activity.perceived_effort if updated_activity.perceived_effort else activity["perceived_effort"]
            activity["elevation_m"] = updated_activity.elevation_m if updated_activity.elevation_m else activity["elevation_m"]
            activity["date_updated"] = updated_activity.date_updated

            return activity

    raise HTTPException(
            status_code=404,
            detail=f"activity with id of {id} does not exist"
        )

@app.delete("/activities/{id}", status_code=204)
async def delete_activity(id: int):
    """endpoint that deletes an activity, according to the given id"""
    for activity in activities:
        if activity["id"] == int(id):
            activities.remove(activity)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)