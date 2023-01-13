import requests

apiUrl = "http://localhost:5000"


def test_questions_management_success():
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

    admin_login = requests.post(f"{apiUrl}/users/login", json={
        "username": "e2eadmin",
        "password": "admin"
    })

    token = admin_login.json().get("auth_token")

    # create question
    question_add_response = requests.post(f"{apiUrl}/questions",
                                          json=question_data,
                                          headers={
                                              "Authorization": f"Bearer {token}"
                                          })

    assert question_add_response.status_code == 201

    # get all questions
    get_questions_result = requests.get(f"{apiUrl}/questions",
                                        headers={
                                            "Authorization": f"Bearer {token}"
                                        })

    assert get_questions_result.status_code == 200

    questions_from_get_all = get_questions_result.json()

    # get by id
    added_id = questions_from_get_all[0].get("id")

    get_question_by_id_result = requests.get(f"{apiUrl}/questions/{added_id}")

    assert get_question_by_id_result.status_code == 200

    # update
    question_update_data = {
        "contents": "How much is 2+5?",
        "answers": [
            {
                "answer_id": "test",
                "text": "5"
            },
            {
                "answer_id": "test2",
                "text": "10"
            },
            {
                "answer_id": "test3",
                "text": "7"
            }
        ],
        "correct_answer_id": "test3"
    }

    update_question_result = requests.put(f"{apiUrl}/questions/{added_id}",
                                          json=question_update_data,
                                          headers={
                                              "Authorization": f"Bearer {token}"
                                          })

    assert update_question_result.status_code == 200

    # delete
    delete_result = requests.delete(f"{apiUrl}/questions/{added_id}",
                                    headers={
                                        "Authorization": f"Bearer {token}"
                                    })

    assert delete_result.status_code == 202

    get_after_delete = requests.get(f"{apiUrl}/questions/{added_id}")

    assert get_after_delete.status_code == 404
