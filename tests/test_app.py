from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app

original_activities = deepcopy(activities)


def reset_activities():
    activities.clear()
    activities.update(deepcopy(original_activities))


def test_get_activities_returns_activity_list():
    # Arrange
    reset_activities()
    client = TestClient(app)
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert expected_activity in data
    assert "participants" in data[expected_activity]


def test_signup_for_activity_adds_participant():
    # Arrange
    reset_activities()
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400():
    # Arrange
    reset_activities()
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"

    first_response = client.post(signup_url, params={"email": email})
    assert first_response.status_code == 200

    # Act
    duplicate_response = client.post(signup_url, params={"email": email})

    # Assert
    assert duplicate_response.status_code == 400
    assert duplicate_response.json() == {"detail": "Student already signed up"}


def test_remove_participant_deletes_participant():
    # Arrange
    reset_activities()
    client = TestClient(app)
    activity_name = "Programming Class"
    email = "removeme@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"
    delete_url = f"/activities/{activity_name}/participants"

    signup_response = client.post(signup_url, params={"email": email})
    assert signup_response.status_code == 200

    # Act
    delete_response = client.delete(delete_url, params={"email": email})

    # Assert
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404():
    # Arrange
    reset_activities()
    client = TestClient(app)
    activity_name = "Programming Class"
    email = "missingstudent@mergington.edu"
    delete_url = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(delete_url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}
