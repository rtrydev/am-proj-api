import uuid

from injector import inject

from domain.models.waypoint import Waypoint
from domain.repositories.waypoint_repository import WaypointRepository
from infrastructure.database.database_provider import DatabaseProvider


class InMemoryWaypointRepository(WaypointRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db_provider = db_provider

    def get_all(self) -> list[Waypoint]:
        db = self.db_provider.get_db()

        if db is None or db.get("waypoints") is None:
            return []

        return [
            Waypoint(waypoint_id, **waypoint_data)
            for waypoint_id, waypoint_data in db["waypoints"].items()
        ]

    def get_by_id(self, waypoint_id: str) -> Waypoint or None:
        db = self.db_provider.get_db()

        if db is None or db.get("waypoints") is None:
            return None

        waypoint_data = db["waypoints"].get(waypoint_id)

        if waypoint_data is None:
            return None

        return Waypoint(waypoint_id, **waypoint_data)

    def add(self, waypoint: dict) -> Waypoint or None:
        db = self.db_provider.get_db()

        if db is None or db.get("waypoints") is None:
            return None

        waypoint_id = str(uuid.uuid4())

        waypoint = {
            "title": waypoint.get("title"),
            "description": waypoint.get("description"),
            "coordinateX": waypoint.get("coordinateX"),
            "coordinateY": waypoint.get("coordinateY")
        }

        db["waypoints"][waypoint_id] = waypoint

        return waypoint

    def update(self, waypoint: dict, waypoint_id: str) -> Waypoint or None:
        db = self.db_provider.get_db()

        if db is None or db.get("waypoints") is None:
            return None

        if waypoint_id is None:
            return None

        db_waypoint = db["waypoints"].get(waypoint_id)

        if db_waypoint is None:
            return None

        db_waypoint["title"] = waypoint.get("title")
        db_waypoint["description"] = waypoint.get("description")
        db_waypoint["coordinateX"] = waypoint.get("coordinateX")
        db_waypoint["coordinateY"] = waypoint.get("coordinateY")

        db["waypoints"][waypoint_id] = db_waypoint

        return db_waypoint

    def delete(self, waypoint_id: str):
        db = self.db_provider.get_db()

        if db is None or db.get("waypoints") is None:
            return

        db_waypoint = db["waypoints"].get(waypoint_id)

        if db_waypoint is None:
            return

        del db["waypoints"][waypoint_id]
