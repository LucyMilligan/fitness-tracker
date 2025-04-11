from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from database.database import create_db_and_tables
from routes import activities, users
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(activities.router, prefix="/activities")
app.include_router(users.router, prefix="/users")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Error handler to catch database errors, such as a foreign key violation
    (e.g. an activity is added with a user_id that doesn't exist in the user_table)"""
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Something went wrong on the server/database. Check your user_id is valid and exists."
        },
    )


@app.get("/")
async def get_api_healthcheck():
    return {"message": "API up and running"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8080)
