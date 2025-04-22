from fastapi.testclient import TestClient
from sqlmodel import Session

from database.models import Activity, User


class TestCreateUser:
    def test_create_user_valid_request_body(self, client: TestClient):
        user_test = {"name": "Test", "email": "test@email"}
        response = client.post("/users/", json=user_test)
        data = response.json()

        assert response.status_code == 201
        assert data["name"] == "Test"
        assert data["user_id"] is not None
        assert data["email"] == "test@email"

    def test_create_user_incomplete_request_body(self, client: TestClient):
        user_test = {"name": "Test"}
        response = client.post("/users/", json=user_test)
        assert response.status_code == 422

    def test_create_user_invalid_request_body(self, client: TestClient):
        user_test = {"name": "Test", "email": 57864587}
        response = client.post("/users/", json=user_test)
        assert response.status_code == 422

    def test_create_user_invalid_email_address(self, client: TestClient):
        user_test = {
            "name": "Test",
            "email": "testemail",
        }  # invalid email (should contain @)
        response = client.post("/users/", json=user_test)
        data = response.json()
        assert response.status_code == 422
        assert "Invalid email address." in data["detail"]


class TestGetUsers:
    def test_get_users(self, session: Session, client: TestClient):
        # add users to the empty database
        user_1 = User(name="test_1", email="test email 1")
        user_2 = User(name="test_2", email="test email 2")
        session.add(user_1)
        session.add(user_2)
        session.commit()

        # test the endpoint
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

    def test_get_user_by_user_id_raises_exception(
        self, session: Session, client: TestClient
    ):
        user_1 = User(name="test_1", email="test email 1")
        session.add(user_1)
        session.commit()

        response = client.get("/users/3")
        data = response.json()

        assert response.status_code == 404
        assert data["detail"] == "User not found"


class TestUpdateUser:
    def test_update_user_updates_user_name(self, session: Session, client: TestClient):
        user_1 = User(name="test_1", email="test@email")
        session.add(user_1)
        session.commit()

        response = client.patch("/users/1", json={"name": "updated"})
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "updated"
        assert data["user_id"] == user_1.user_id
        assert "email" not in data

    def test_update_user_raises_422_error_for_incorrect_email_format(
        self, session: Session, client: TestClient
    ):
        user_1 = User(name="test_1", email="test@email")
        session.add(user_1)
        session.commit()

        response = client.patch(
            "/users/1", json={"name": "updated", "email": "updated_email"}
        )  # email missing @
        data = response.json()

        assert response.status_code == 422
        assert "Invalid email address." in data["detail"][0]["msg"]


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


class TestGetActivitiesByUserId:
    def test_endpoint_responds_with_specific_user_id_activities(
        self, session: Session, client: TestClient, activity_test_1, activity_test_2
    ):
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


class TestGetActivitiesToPlotByUserId:
    def test_endpoint_responds_with_with_additional_fields_default_dates(
        self, session: Session, client: TestClient, activity_test_1, activity_test_2
    ):
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()

        response = client.get("/users/1/activities-to-plot")
        response_activities = response.json()

        assert isinstance(response_activities, list)
        for activity in response_activities:
            assert activity["user_id"] == 1
            assert "pace_str_mps" in activity
            assert "pace_float_mps" in activity
            assert "speed_kmphr" in activity
            assert "formatted_time" in activity

    def test_endpoint_responds_with_activities_between_given_dates(
        self, session: Session, client: TestClient, activity_test_1, activity_test_2
    ):
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()

        start_date = "2010/09/01"
        end_date = "2010/11/01"
        response = client.get(f"/users/1/activities-to-plot?start_date={start_date}&end_date={end_date}")
        response_activities = response.json()

        assert len(response_activities) == 1
        for activity in response_activities:
            assert activity["date"] < "2010/11/01" and activity["date"] > "2010/09/01"

    def test_invalid_user_id_raises_404_error(self, client: TestClient):
        response = client.get("/users/-1/activities-to-plot")
        assert response.status_code == 404
        assert response.json()["detail"] == "No activities found"

    def test_dates_out_of_range_raises_404_error(
        self, session: Session, client: TestClient, activity_test_1, activity_test_2
    ):
        activity_1 = Activity(**activity_test_1)
        activity_2 = Activity(**activity_test_2)
        session.add(activity_1)
        session.add(activity_2)
        session.commit()

        start_date = "2000/09/01"
        end_date = "2000/11/01"
        response = client.get(f"/users/1/activities-to-plot?start_date={start_date}&end_date={end_date}")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "No activities found"