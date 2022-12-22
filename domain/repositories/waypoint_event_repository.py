from abc import ABC, abstractmethod

from domain.models.waypoint_event import WaypointEvent


class WaypointEventRepository(ABC):
    @abstractmethod
    def event_for_waypoint_exists(self, user_id, waypoint_id) -> bool:
        pass

    @abstractmethod
    def get_waypoint_events_for_user(self, user_id) -> list[WaypointEvent]:
        pass

    @abstractmethod
    def get_by_id(self, event_id) -> WaypointEvent or None:
        pass

    @abstractmethod
    def add(self, event: WaypointEvent) -> WaypointEvent or None:
        pass

    @abstractmethod
    def update(self, event: WaypointEvent) -> WaypointEvent or None:
        pass
