import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app, get_session
from models import Activity, User


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
        "elevation_m": 15
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
        "elevation_m": 10
    }


class TestCreateUser:
    def test_create_user_valid_request_body(self, client: TestClient):
        user_test = {"name": "Test", "email": "test email"}
        response = client.post("/users/", json=user_test)
        data = response.json()

        assert response.status_code == 201
        assert data["name"] == "Test"
        assert data["user_id"] is not None
        assert data["email"] == "test email"

    def test_create_user_incomplete_request_body(self, client: TestClient):
        user_test = {"name": "Test"}
        response = client.post("/users/", json=user_test)
        assert response.status_code == 422

    def test_create_user_invalid_request_body(self, client: TestClient):
        user_test = {"name": "Test", "email": 57864587}
        response = client.post("/users/", json=user_test)
        assert response.status_code == 422


class TestGetUsers:
    def test_get_users(self, session: Session, client: TestClient):
        #add users to the empty database
        user_1 = User(name="test_1", email="test email 1")
        user_2 = User(name="test_2", email="test email 2")
        session.add(user_1)
        session.add(user_2)
        session.commit()

        #test the endpoint
        response = client.get("/users/")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]["name"] == user_1.name
        assert data[1]["name"] == user_2.name
        for user in data:
            assert "email" not in user
            assert user["user_id"] is not None


class TestGetUserByUserId:
    def test_get_user_by_user_id(self, session: Session, client: TestClient):
        user_1 = User(name="test_1", email="test email 1")
        session.add(user_1)
        session.commit()

        response = client.get("/users/1")
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == user_1.name
        assert data["user_id"] == 1

    def test_get_user_by_user_id_raises_exception(self, session: Session, client: TestClient):
        user_1 = User(name="test_1", email="test email 1")
        session.add(user_1)
        session.commit()

        response = client.get("/users/3")
        data = response.json()

        assert response.status_code == 404
        assert data["detail"] == "User not found"


class TestUpdateUser:
    def test_update_user_updates_user(self, session: Session, client: TestClient):
        user_1 = User(name="test_1", email="test email 1")
        session.add(user_1)
        session.commit()

        response = client.patch("/users/1", json={"name": "updated"})
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "updated"
        assert data["user_id"] == user_1.user_id
        assert "email" not in data


class TestDeleteUser:
    def test_delete_user_deletes_user(self, session: Session, client: TestClient):
        user_1 = User(name="test_1", email="test email 1")
        session.add(user_1)
        session.commit()

        response = client.delete("/users/1")
        data = response.json()
        users_in_db = session.get(User, 1)

        assert response.status_code == 200
        assert users_in_db is None
        assert data == {"message": "User_id 1 deleted"}


class TestGetActivities:
    def test_get_activities(self, session: Session, client: TestClient, activity_test_1, activity_test_2):
        #add activities to the empty database
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()

        #test the endpoint
        response = client.get("/activities/")
        response_activities = response.json()

        assert response.status_code == 200
        assert isinstance(response_activities, list)
        assert len(response_activities) == 2
        assert response_activities[0]["id"] == 1
        assert response_activities[1]["id"] == 2
        assert response_activities[0]["perceived_effort"] == 10
        assert response_activities[1]["perceived_effort"] == 8
        assert response_activities[0]["activity"] == "run"
        assert response_activities[1]["activity"] == "run"

    
    def test_get_users_sorted_by_default_id_asc(self, session: Session, client: TestClient, activity_test_1, activity_test_2):
        #add activities to the empty database
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()

        #test the endpoint
        response = client.get("/activities/")
        response_activities = response.json()

        assert response_activities[0]["id"] < response_activities[-1]["id"]


    def test_endpoint_sorted_by_distance_desc(self, session: Session, client: TestClient, activity_test_1, activity_test_2):
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()

        response = client.get("activities?sort_by=distance_km&order_by=desc")
        response_activities = response.json()
        
        assert response_activities[0]["distance_km"] > response_activities[-1]["distance_km"]


    def test_endpoint_limited_to_one_activity(self, session: Session, client: TestClient, activity_test_1, activity_test_2):
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()

        response = client.get("activities?offset=0&limit=1")
        response_activities = response.json()
        
        assert len(response_activities) == 1


    def test_invalid_endpoint_raises_404_error(self, client: TestClient):
        response = client.get("/actvts")
        assert response.status_code == 404

    def test_invalid_query_raises_422_error(self, client: TestClient):
        response = client.get("activities?sort_by=testing&order_by=desc")
        assert response.status_code == 422


class TestGetActivitiesById:
    def test_endpoint_responds_with_appropriate_activity_id(self, session: Session, client: TestClient, activity_test_1, activity_test_2):
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()

        response = client.get("/activities/1")
        response_activity = response.json()

        assert response_activity["id"] == 1

    def test_invalid_id_raises_404_error(self, client: TestClient):
        response = client.get("/activities/-1")
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestGetActivitiesByUserId:
    def test_endpoint_responds_with_specific_user_id_activities(self, session: Session, client: TestClient, activity_test_1, activity_test_2):
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()

        response = client.get("/users/1/activities")
        response_activities = response.json()

        assert isinstance(response_activities, list)
        for activity in response_activities:
            assert activity["user_id"] == 1


    def test_invalid_user_id_raises_404_error(self, client: TestClient):
        response = client.get("/users/-1/activities")
        assert response.status_code == 404
        assert response.json()["detail"] == "No activities found"


class TestPostActivity:
    def test_endpoint_returns_201_status_code_on_success(self, client: TestClient, activity_test_1):
        response = client.post("/activities/", json=activity_test_1)
        assert response.status_code == 201


    def test_endpoint_returns_added_activity(self, client: TestClient, activity_test_1):
        response = client.post("/activities/", json=activity_test_1)
        new_activity = response.json()
        activity_test_1["id"] = 1
        assert new_activity == activity_test_1


    def test_endpoint_raises_422_error_if_request_body_incomplete(self, client: TestClient):
        activity_test = {"id": 3, "distance": 4.4}
        response = client.post("/activities", json=activity_test)
        assert response.status_code == 422


class TestPatchActivity:
    def test_endpoint_returns_200_status_code_on_success(self, client: TestClient, session: Session, activity_test_1):
        activity_1 = Activity(**activity_test_1)
        session.add(activity_1)
        session.commit()
        
        activity_patch_test = {"distance_km": 15, "activity_type": "road"}
        response = client.patch("/activities/1", json=activity_patch_test)
        assert response.status_code == 200


    def test_endpoint_returns_correctly_updated_activity_when_selected_fields_updated(self, client: TestClient, session: Session, activity_test_1):
        activity_1 = Activity(**activity_test_1)
        session.add(activity_1)
        session.commit()
        
        activity_patch_test = {"distance_km": 15, "activity_type": "road"}
        response = client.patch("/activities/1", json=activity_patch_test)
        response_activities = response.json()

        assert response_activities["distance_km"] == 15
        assert response_activities["activity_type"] == "road"
        assert response_activities["user_id"] #testing that non-updated fields are not null


    def test_invalid_id_raises_404_error(self, client: TestClient):
        response = client.get("/activities/-1")
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestDeleteActivity:
    def test_endpoint_returns_204_status_code_upon_deletion(self, client: TestClient, session: Session, activity_test_1):
        activity_1 = Activity(**activity_test_1)
        session.add(activity_1)
        session.commit()

        response = client.delete("/activities/1")
        data = response.json()
        activities_in_db = session.get(Activity, 1)

        assert response.status_code == 200
        assert activities_in_db is None
        assert data == {"message": "Activity id 1 deleted"}

    def test_activity_deleted(self, session: Session, client: TestClient, activity_test_1, activity_test_2):
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()
        
        response_before = client.get("/activities")
        response_before_del = response_before.json()

        client.delete("/activities/2")
        response_after = client.get("/activities")
        response_after_del = response_after.json()

        assert len(response_before_del) == len(response_after_del) + 1
        for activity in response_after_del:
            assert activity["id"] != 2
