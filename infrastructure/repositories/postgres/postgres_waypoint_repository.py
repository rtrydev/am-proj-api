from injector import inject

from infrastructure.models.waypoint import Waypoint as WaypointModel
from domain.models.waypoint import Waypoint
from domain.repositories.waypoint_repository import WaypointRepository
from infrastructure.database.database_provider import DatabaseProvider


class PostgresWaypointRepository(WaypointRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db = db_provider.get_db()

    def get_all(self) -> list[Waypoint]:
        result = self.db.query(WaypointModel)

        return [
            Waypoint(
                id=item.id,
                title=item.title,
                description=item.description,
                coordinateX=item.coordinateX,
                coordinateY=item.coordinateY
            ) for item in result
        ]

    def get_by_id(self, waypoint_id: str) -> Waypoint or None:
        result = self.db.query(WaypointModel).filter_by(id=waypoint_id).one_or_none()

        if result is None:
            return None

        waypoint = Waypoint(
            id=result.id,
            title=result.title,
            description=result.description,
            coordinateX=result.coordinateX,
            coordinateY=result.coordinateY
        )

        return waypoint

    def add(self, waypoint: dict) -> Waypoint or None:
        pass

    def update(self, waypoint: dict, waypoint_id: str) -> Waypoint or None:
        pass

    def delete(self, waypoint_id: str):
        pass
