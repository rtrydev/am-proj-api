from domain.enums.roles import Roles
from infrastructure.database.database_provider import DatabaseProvider


class InMemoryDatabaseProvider(DatabaseProvider):
    data = {
        "waypoints": {
            "58fce52a-87bc-43d8-8163-54fb66fbb4af": {
                "title": "waypoint 1",
                "description": "near xyz",
                "coordinateX": 12.1234,
                "coordinateY": 54.1235
            },
            "3d876547-c33f-471e-a956-28b4827ea605": {
                "title": "waypoint 2",
                "description": "near abc",
                "coordinateX": 15.1234,
                "coordinateY": 44.1235
            },
            "30defd48-cfb2-4f9e-9c87-e3742e47d041": {
                "title": "waypoint 3",
                "description": "near qwe",
                "coordinateX": 22.1234,
                "coordinateY": 24.1235
            }
        },
        "questions": {
            "9aa37887-7360-4d12-82c5-67a3d2a96833": {
                "contents": "2+4?",
                "answers": [
                    {
                        "answer_id": "a42ed6ce-a264-4683-8dba-9895e2aff5a5",
                        "text": "3"
                    },
                    {
                        "answer_id": "ba08dff4-515c-4c16-ac78-611733e58a7a",
                        "text": "6"
                    },
                    {
                        "answer_id": "d6b242a6-395b-4be0-b058-e9e53c5b33e0",
                        "text": "-14"
                    },
                ],
                "correct_answer_id": "ba08dff4-515c-4c16-ac78-611733e58a7a"
            }
        },
        "users": {
            "7215f897-2ef5-4359-86bc-06aed1c2b811": {
                "username": "rtry",
                "password": "$2b$12$ZB81eVxtSN2ZFNmgC0s/6OzOtVtagEDh7aPfh5rHSClYbQJOq5JNK".encode("utf-8"),
                "role": Roles.Admin,
                "question_answers": []
            }
        },
        "question_answers": {
            "8411884b-2325-4e84-a327-b8fa47ff4a9e": {
                "user_id": "7215f897-2ef5-4359-86bc-06aed1c2b811",
                "question_id": "9aa37887-7360-4d12-82c5-67a3d2a96833",
                "answer_id": "ba08dff4-515c-4c16-ac78-611733e58a7a"
            }
        }
    }

    def get_db(self):
        return self.data
