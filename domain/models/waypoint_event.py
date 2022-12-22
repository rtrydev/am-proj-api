from dataclasses import dataclass

from domain.enums.event_states import EventStates
from domain.models.question import Question
from domain.models.user import User
from domain.models.waypoint import Waypoint


@dataclass
class WaypointEvent:
    id: str
    timestamp: int
    waypoint: Waypoint
    user: User
    question: Question or None
    state: EventStates
