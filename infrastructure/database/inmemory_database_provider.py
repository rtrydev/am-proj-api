from domain.enums.roles import Roles
from infrastructure.database.database_provider import DatabaseProvider


class InMemoryDatabaseProvider(DatabaseProvider):
    data = {
        "waypoints": {
            "test1": {
                "title": "waypoint 1",
                "description": "near xyz",
                "coordinateX": 12.1234,
                "coordinateY": 54.1235
            },
            "test2": {
                "title": "waypoint 2",
                "description": "near abc",
                "coordinateX": 15.1234,
                "coordinateY": 44.1235
            },
            "test3": {
                "title": "waypoint 3",
                "description": "near qwe",
                "coordinateX": 22.1234,
                "coordinateY": 24.1235
            }
        },
        "questions": {},
        "users": {
            "test1": {
                "username": "test",
                "password": "Test",
                "role": Roles.User
            },
            "test2": {
                "username": "admin",
                "password": "admin",
                "role": Roles.Admin
            }
        }
    }

    def get_db(self):
        return self.data
