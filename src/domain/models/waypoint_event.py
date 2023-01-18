from dataclasses import dataclass

from src.domain.enums.event_states import EventStates
from src.domain.models.question import Question
from src.domain.models.user import User
from src.domain.models.waypoint import Waypoint


@dataclass
class WaypointEvent:
    id: str
    timestamp: int
    waypoint: Waypoint
    user: User
    question: Question or None
    answer_correct: bool or None
    state: EventStates
