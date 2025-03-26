from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from database import create_db_and_tables
from routes import activities, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(activities.router, prefix="/activities")
app.include_router(users.router, prefix="/users")

@app.get("/")
async def get_api_healthcheck():
    return {"message": "API up and running"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8080)