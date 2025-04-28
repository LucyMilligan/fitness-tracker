import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from database.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    """fixture to create the custom engine for testing purposes,
    create the tables, and create the session.
    SQLite used rather than Postgres for ease/speed of testing, as the
    database can be stored in-memory"""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """fixture to tell fastAPI to use get_session_override (test session) instead of
    get_session (production session). After the test function is done, pytest will
    come back to execute the rest of the code after yield"""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def activity_test_1(scope="function"):
    return {
        "user_id": 1,
        "date": "2010-10-10",
        "time": "10:00",
        "activity": "run",
        "activity_type": "trail",
        "moving_time": "00:35:00",
        "distance_km": 5.0,
        "perceived_effort": 10,
        "elevation_m": 15,
    }


@pytest.fixture
def activity_test_2(scope="function"):
    return {
        "user_id": 1,
        "date": "2011-10-10",
        "time": "10:00",
        "activity": "run",
        "activity_type": "trail",
        "moving_time": "01:00:00",
        "distance_km": 10.0,
        "perceived_effort": 8,
        "elevation_m": 10,
    }
