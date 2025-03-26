from fastapi.testclient import TestClient
from sqlmodel import Session

from models import Activity


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
