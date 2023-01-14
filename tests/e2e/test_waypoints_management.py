import pytest
import requests
import subprocess
import time

apiUrl = "http://localhost:5000"


@pytest.fixture(autouse=True)
def run_around_tests():
    subprocess.call(['sh', './tests/e2e/reset_database.sh'])
    time.sleep(2)


@pytest.mark.e2e
def test_waypoints_management_success():
    waypoint_data = {
        "title": "test123",
        "description": "some desc",
        "coordinateX": 12.5432,
        "coordinateY": 65.1233
    }

    admin_login = requests.post(f"{apiUrl}/users/login", json={
        "username": "e2eadmin",
        "password": "admin"
    })

    token = admin_login.json().get("auth_token")

    # create waypoint
    waypoint_add_response = requests.post(f"{apiUrl}/waypoints",
                                          json=waypoint_data,
                                          headers={
                                              "Authorization": f"Bearer {token}"
                                          })

    assert waypoint_add_response.status_code == 201

    # get all waypoints
    get_waypoints_result = requests.get(f"{apiUrl}/waypoints")

    assert get_waypoints_result.status_code == 200

    waypoints_from_get_all = get_waypoints_result.json()
    expected = [
        {
            "id": waypoints_from_get_all[0].get("id") or "noid",
            **waypoint_data
        }
    ]

    assert get_waypoints_result.json() == expected

    # get by id
    added_id = waypoints_from_get_all[0].get("id")

    get_waypoint_by_id_result = requests.get(f"{apiUrl}/waypoints/{added_id}")
    expected = {
        "id": waypoints_from_get_all[0].get("id") or "noid",
        **waypoint_data
    }

    assert get_waypoint_by_id_result.status_code == 200
    assert get_waypoint_by_id_result.json() == expected

    # update
    waypoint_update_data = {
        "title": "test312",
        "description": "desc",
        "coordinateX": 42.5432,
        "coordinateY": 63.1233
    }

    update_waypoint_result = requests.put(f"{apiUrl}/waypoints/{added_id}",
                                          json=waypoint_update_data,
                                          headers={
                                              "Authorization": f"Bearer {token}"
                                          })

    assert update_waypoint_result.status_code == 200

    get_after_update = requests.get(f"{apiUrl}/waypoints/{added_id}")
    expected = {
        "id": added_id,
        **waypoint_update_data
    }

    assert get_after_update.json() == expected

    # delete
    delete_result = requests.delete(f"{apiUrl}/waypoints/{added_id}",
                                    headers={
                                        "Authorization": f"Bearer {token}"
                                    })

    assert delete_result.status_code == 202

    get_after_delete = requests.get(f"{apiUrl}/waypoints/{added_id}")

    assert get_after_delete.status_code == 404
