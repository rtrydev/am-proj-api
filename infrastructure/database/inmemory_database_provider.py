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
        "questions": {},
        "users": {
            "7215f897-2ef5-4359-86bc-06aed1c2b811": {
                "username": "rtry",
                "password": "$2b$12$ZB81eVxtSN2ZFNmgC0s/6OzOtVtagEDh7aPfh5rHSClYbQJOq5JNK".encode("utf-8"),
                "role": Roles.Admin,
                "question_answers": []
            }
        }
    }

    def get_db(self):
        return self.data
