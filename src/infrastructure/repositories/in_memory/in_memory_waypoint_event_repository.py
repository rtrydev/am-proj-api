from injector import inject

from src.domain.models.question import Question
from src.domain.models.user import User
from src.domain.models.waypoint import Waypoint
from src.domain.models.waypoint_event import WaypointEvent
from src.domain.repositories.waypoint_event_repository import WaypointEventRepository
from src.infrastructure.database.database_provider import DatabaseProvider


class InMemoryWaypointEventRepository(WaypointEventRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db_provider = db_provider

    def event_for_waypoint_exists(self, user_id, waypoint_id) -> bool:
        db = self.db_provider.get_db()

        if db is None or db.get("events") is None:
            return False

        event_exists = any(
            {
                "user_id": event.get("user_id"),
                "waypoint_id": event.get("waypoint_id")
            }
            for key, event in db["events"].items()
            if event.get("user_id") == user_id
            and event.get("waypoint_id") == waypoint_id
        )

        return event_exists

    def get_waypoint_events_for_user(self, user_id) -> list[WaypointEvent]:
        db = self.db_provider.get_db()

        if db is None or db.get("events") is None:
            return []

        result = [
            self._create_event({
                "id": event_id,
                **event_data
            }, db)
            for event_id, event_data in db["events"].items()
            if event_data.get("user_id") == user_id
        ]

        return result

    def get_by_id(self, event_id) -> WaypointEvent or None:
        db = self.db_provider.get_db()

        if db is None or db.get("events") is None:
            return None

        db_event = db["events"].get(event_id)

        if db_event is None:
            return None

        return self._create_event(
            {
                "id": event_id,
                **db_event
            },
            db
        )

    def add(self, event: WaypointEvent) -> WaypointEvent or None:
        db = self.db_provider.get_db()

        if db is None or db.get("events") is None:
            return None

        db_event = {
            "timestamp": event.timestamp,
            "waypoint_id": event.waypoint.id,
            "user_id": event.user.id,
            "question_id": "",
            "state": event.state
        }

        db["events"][event.id] = db_event

        return event

    def update(self, event: WaypointEvent) -> WaypointEvent or None:
        db = self.db_provider.get_db()

        if db is None or db.get("events") is None:
            return None

        if db["events"].get(event.id) is None:
            return None

        db_event = {
            "timestamp": event.timestamp,
            "waypoint_id": event.waypoint.id,
            "user_id": event.user.id,
            "question_id": event.question.id if event.question is not None else None,
            "state": event.state,
            "answer_correct": event.answer_correct
        }

        db["events"][event.id] = db_event

        return event

    def _create_event(self, event_data: dict, db) -> WaypointEvent:
        db_user = User(
            id=event_data.get("user_id"),
            **db["users"].get(event_data.get("user_id"))
        )

        db_waypoint = Waypoint(
            id=event_data.get("waypoint_id"),
            **db["waypoints"].get(event_data.get("waypoint_id"))
        )

        question_exists = db["questions"].get(event_data.get("question_id")) is not None
        db_question = Question(
            id=event_data.get("question_id"),
            **db["questions"].get(event_data.get("question_id"))
        ) if question_exists else None

        return WaypointEvent(
            id=event_data.get("id"),
            timestamp=event_data.get("timestamp"),
            user=db_user,
            waypoint=db_waypoint,
            question=db_question,
            answer_correct=event_data.get("answer_correct"),
            state=event_data.get("state")
        )