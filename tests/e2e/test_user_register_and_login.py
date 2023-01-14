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
def test_user_register_and_login_success():
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    register_response = requests.post(f"{apiUrl}/users/register", json=user_data)

    assert register_response.status_code == 201

    login_response = requests.post(f"{apiUrl}/users/login", json=user_data)

    auth_token = login_response.json().get("auth_token")

    assert login_response.status_code == 200
    assert auth_token is not None

    get_user_response = requests.get(f"{apiUrl}/users", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    user = get_user_response.json()

    expected = {
        "id": user.get("id") or "noid",
        "username": "testuser",
        "role": 0
    }

    assert get_user_response.status_code == 200
    assert user == expected


@pytest.mark.e2e
def test_user_login_incorrect_credentials_fail():
    user_data = {
        "username": "somenonexistent",
        "password": "testpassword"
    }

    login_response = requests.post(f"{apiUrl}/users/login", json=user_data)

    assert login_response.status_code == 404


@pytest.mark.e2e
def test_get_user_unauthorized_fail():
    get_user_response = requests.get(f"{apiUrl}/users")

    assert get_user_response.status_code == 401
