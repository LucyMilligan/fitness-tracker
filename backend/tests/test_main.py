import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def test_client(scope="function"):
    return TestClient(app)

@pytest.fixture
def activity_test(scope="function"):
    return {
        "id": 10,
        "user_id": 10,
        "date": "2010-10-10",
        "time": "10:00",
        "activity": "run",
        "activity_type": "trail",
        "moving_time": "01:00:00",
        "distance_km": 10.0,
        "perceived_effort": 10,
        "elevation_m": 10,
        "date_updated": "2020-10-10T10:00:00"
    }

@pytest.fixture
def activity_patch_test(scope="function"):
    return {
        "user_id": 1,
        "date": "2010-10-10",
        "time": "10:00",
        "activity": "run",
        "activity_type": "trail",
        "moving_time": "01:00:00",
        "distance_km": 10.0,
        "perceived_effort": 10,
        "elevation_m": 10,
        "date_updated": "2020-10-10T10:00:00"
    }

class TestGetActivities:
    def test_endpoint_responds_with_all_activities(self, test_client):
        response = test_client.get("/activities")
        response_activities = response.json()
        assert response.status_code == 200
        assert isinstance(response_activities, list)
        assert len(response_activities) > 0
        for activity in response_activities:
            assert isinstance(activity["id"], int)
            assert isinstance(activity["time"], str)
            assert isinstance(activity["perceived_effort"], int)


    def test_endpoint_sorted_by_default_id_asc(self, test_client):
        response = test_client.get("/activities")
        response_activities = response.json()
        assert response_activities[0]["id"] < response_activities[-1]["id"]


    def test_endpoint_sorted_by_distance_desc(self, test_client):
        response = test_client.get("activities?sort_by=distance_km&order_by=desc")
        response_activities = response.json()
        assert response_activities[0]["distance_km"] > response_activities[-1]["distance_km"]


    def test_endpoint_limited_to_one_activity(self, test_client):
        response = test_client.get("activities?skip=0&limit=1")
        response_activities = response.json()
        assert len(response_activities) == 1


    def test_invalid_endpoint_raises_404_error(self, test_client):
        response = test_client.get("/actvts")
        assert response.status_code == 404

    def test_invalid_query_raises_422_error(self, test_client):
        response = test_client.get("activities?sort_by=testing&order_by=desc")
        assert response.status_code == 422


class TestGetActivitiesById:
    def test_endpoint_responds_with_appropriate_activity_id(self, test_client):
        response = test_client.get("/activities/1")
        response_activity = response.json()
        assert response_activity["id"] == 1

    def test_invalid_id_raises_404_error(self, test_client):
        response = test_client.get("/activities/-1")
        assert response.status_code == 404
        assert response.json()["detail"] == "activity with id of -1 does not exist"


class TestGetActivitiesByUserId:
    def test_endpoint_responds_with_specific_user_id_activities(self, test_client):
        response = test_client.get("/users/1/activities")
        response_activities = response.json()
        assert isinstance(response_activities, list)
        for activity in response_activities:
            assert activity["user_id"] == 1


    def test_invalid_user_id_raises_404_error(self, test_client):
        response = test_client.get("/users/-1/activities")
        assert response.status_code == 404
        assert response.json()["detail"] == "no activities recorded for user_id -1"


class TestPostActivity:
    def test_endpoint_returns_201_status_code_on_success(self, test_client, activity_test):
        response = test_client.post("/activities", json=activity_test)
        assert response.status_code == 201


    def test_endpoint_returns_added_treasure(self, test_client, activity_test):
        response = test_client.post("/activities", json=activity_test)
        new_activity = response.json()
        assert new_activity == activity_test

    def test_endpoint_raises_422_error_if_request_body_incomplete(self, test_client):
        activity_test = {"id": 3, "distance": 4.4}
        response = test_client.post("/activities", json=activity_test)
        assert response.status_code == 422


class TestPatchActivity:
    def test_endpoint_returns_200_status_code_on_success(self, test_client, activity_patch_test):
        response = test_client.patch("/activities/1", json=activity_patch_test)
        assert response.status_code == 200

    def test_endpoint_returns_updated_activity_when_all_fields_updated(self, test_client, activity_patch_test):
        response = test_client.patch("/activities/1", json=activity_patch_test)
        response_activities = response.json()
        assert response_activities == {
            "id": 1,
            "user_id": 1,
            "date": "2010-10-10",
            "time": "10:00",
            "activity": "run",
            "activity_type": "trail",
            "moving_time": "01:00:00",
            "distance_km": 10.0,
            "perceived_effort": 10,
            "elevation_m": 10,
            "date_updated": "2020-10-10T10:00:00"
        }


    def test_endpoint_returns_correctly_updated_activity_when_selected_fields_updated(self, test_client):
        activity_patch_test = {"perceived_effort": 9, "date_updated": "2020-10-10T10:00:00"}
        response = test_client.patch("/activities/1", json=activity_patch_test)
        response_activities = response.json()
        assert response_activities["perceived_effort"] == 9
        assert response_activities["date_updated"] == "2020-10-10T10:00:00"
        assert response_activities["user_id"] #testing that non-updated fields are not null

    def test_invalid_id_raises_404_error(self, test_client):
        response = test_client.get("/activities/-1")
        assert response.status_code == 404
        assert response.json()["detail"] == "activity with id of -1 does not exist"

#to improve - make sure each test resets
class TestDeleteActivity:
    def test_endpoint_returns_204_status_code_upon_deletion(self, test_client):
        response = test_client.delete("/activities/1")
        assert response.status_code == 204

    def test_number_of_activities_decreases_after_deletion(self, test_client):
        response_before = test_client.get("/activities")
        response_before_del = response_before.json()
        test_client.delete("/activities/2")
        response_after = test_client.get("/activities")
        response_after_del = response_after.json()
        assert len(response_before_del) == len(response_after_del) + 1

    def test_endpoint_deletes_correct_activity(self, test_client):
        test_client.delete("/activities/1")
        response_after = test_client.get("/activities")
        response_after_del = response_after.json()
        for activity in response_after_del:
            assert activity["id"] != 1