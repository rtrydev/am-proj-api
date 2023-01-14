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
def test_question_answer_flow():
    question_data = {
        "contents": "How much is 2+5?",
        "answers": [
            {
                "answer_id": "test",
                "text": "5"
            },
            {
                "answer_id": "test2",
                "text": "7"
            },
            {
                "answer_id": "test3",
                "text": "-18"
            }
        ],
        "correct_answer_id": "test2"
    }

    waypoint_data = {
        "title": "test321",
        "description": "some desc",
        "coordinateX": 13.5432,
        "coordinateY": 45.1233
    }

    admin_login = requests.post(f"{apiUrl}/users/login", json={
        "username": "e2eadmin",
        "password": "admin"
    })

    admin_token = admin_login.json().get("auth_token")

    requests.post(f"{apiUrl}/waypoints",
                  json=waypoint_data,
                  headers={
                      "Authorization": f"Bearer {admin_token}"
                  })

    requests.post(f"{apiUrl}/questions",
                  json=question_data,
                  headers={
                      "Authorization": f"Bearer {admin_token}"
                  })

    get_waypoints_result = requests.get(f"{apiUrl}/waypoints")
    waypoint_id = get_waypoints_result.json()[0].get("id")

    user_login = requests.post(f"{apiUrl}/users/login", json={
        "username": "e2euser",
        "password": "admin"
    })
    user_token = user_login.json().get("auth_token")

    waypoint_event = requests.post(f"{apiUrl}/waypoint_events",
                                   json={
                                       "waypoint_id": waypoint_id
                                   },
                                   headers={
                                       "Authorization": f"Bearer {user_token}"
                                   })

    assert waypoint_event.status_code == 200

    waypoint_event_id = waypoint_event.json().get("event_id")

    get_event_question_result = requests.get(f"{apiUrl}/waypoint_events/{waypoint_event_id}/question",
                                             headers={
                                                 "Authorization": f"Bearer {user_token}"
                                             })

    assert get_event_question_result.status_code == 200

    question = get_event_question_result.json()

    answer_question_payload = {
        "question_id": question.get("id"),
        "answer_id": question.get("answers")[0].get("id"),
        "event_id": waypoint_event_id
    }

    answer_question_result = requests.post(f"{apiUrl}/question_answers",
                                           json=answer_question_payload,
                                           headers={
                                               "Authorization": f"Bearer {user_token}"
                                           })

    assert answer_question_result.status_code == 201
