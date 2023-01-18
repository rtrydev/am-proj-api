from injector import inject
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.models.waypoint import Waypoint as WaypointModel
from src.domain.models.waypoint import Waypoint
from src.domain.repositories.waypoint_repository import WaypointRepository
from src.infrastructure.database.database_provider import DatabaseProvider


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
        waypoint_model = WaypointModel(
            title=waypoint.get("title"),
            description=waypoint.get("description"),
            coordinateX=waypoint.get("coordinateX"),
            coordinateY=waypoint.get("coordinateY")
        )

        result = None

        try:
            self.db.add(waypoint_model)
        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
            self.db.refresh(waypoint_model)

            result = Waypoint(
                id=waypoint_model.id,
                title=waypoint_model.title,
                description=waypoint_model.description,
                coordinateX=waypoint_model.coordinateX,
                coordinateY=waypoint_model.coordinateY
            )
        finally:
            self.db.close()

        return result

    def update(self, waypoint: dict, waypoint_id: str) -> Waypoint or None:
        waypoint_model = self.db.query(WaypointModel).filter_by(id=waypoint_id).one_or_none()

        if waypoint_model is None:
            return None

        waypoint_model.title = waypoint.get("title")
        waypoint_model.description = waypoint.get("description")
        waypoint_model.coordinateX = waypoint.get("coordinateX")
        waypoint_model.coordinateY = waypoint.get("coordinateY")

        result = None

        try:
            self.db.add(waypoint_model)
        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
            self.db.refresh(waypoint_model)

            result = Waypoint(
                id=waypoint_model.id,
                title=waypoint_model.title,
                description=waypoint_model.description,
                coordinateX=waypoint_model.coordinateX,
                coordinateY=waypoint_model.coordinateY
            )
        finally:
            self.db.close()

        return result

    def delete(self, waypoint_id: str):
        waypoint_model = self.db.query(WaypointModel).filter_by(id=waypoint_id).one_or_none()

        if waypoint_model is None:
            return

        try:
            self.db.delete(waypoint_model)
        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
        finally:
            self.db.close()
