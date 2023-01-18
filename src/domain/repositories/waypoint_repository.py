from abc import ABC, abstractmethod
from src.domain.models.waypoint import Waypoint


class WaypointRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Waypoint]:
        pass

    @abstractmethod
    def get_by_id(self, waypoint_id: str) -> Waypoint or None:
        pass

    @abstractmethod
    def add(self, waypoint: dict) -> Waypoint or None:
        pass

    @abstractmethod
    def update(self, waypoint: dict, waypoint_id: str) -> Waypoint or None:
        pass

    @abstractmethod
    def delete(self, waypoint_id: str):
        pass
