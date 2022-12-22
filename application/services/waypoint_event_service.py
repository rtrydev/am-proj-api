import datetime
import uuid
import random

from injector import inject

from domain.enums.event_states import EventStates
from domain.models.waypoint_event import WaypointEvent
from domain.repositories.question_repository import QuestionRepository
from domain.repositories.users_repository import UsersRepository
from domain.repositories.waypoint_event_repository import WaypointEventRepository
from domain.repositories.waypoint_repository import WaypointRepository
from domain.services.waypoint_event_service import WaypointEventServiceInterface


class WaypointEventService(WaypointEventServiceInterface):
    @inject
    def __init__(self,
                 waypoint_event_repository: WaypointEventRepository,
                 users_repository: UsersRepository,
                 question_repository: QuestionRepository,
                 waypoint_repository: WaypointRepository
                 ):
        self.waypoint_event_repository = waypoint_event_repository
        self.users_repository = users_repository
        self.question_repository = question_repository
        self.waypoint_repository = waypoint_repository

    def get_random_question_for_event(self, event_id, user_id):
        event = self.waypoint_event_repository.get_by_id(event_id)

        if event is None:
            return None

        if event.user.id != user_id:
            return None

        if event.state != EventStates.Initialized:
            return None

        event.state = EventStates.QuestionReceived
        result = self.waypoint_event_repository.update(event)

        if result is None:
            return None

        questions = self.question_repository.get_all()
        selected_question = random.choice(questions)

        event.question = selected_question
        self.waypoint_event_repository.update(event)

        return selected_question

    def init_waypoint_event(self, waypoint_id, user_id):
        user = self.users_repository.get_by_id(user_id)

        if user is None:
            return None

        waypoint = self.waypoint_repository.get_by_id(waypoint_id)

        if waypoint is None:
            return None

        event_exists = self.waypoint_event_repository.event_for_waypoint_exists(
            user_id,
            waypoint_id
        )

        if event_exists:
            return None

        event_id = str(uuid.uuid4())
        timestamp = int(datetime.datetime.now().timestamp())

        event = WaypointEvent(
            id=event_id,
            timestamp=timestamp,
            waypoint=waypoint,
            user=user,
            question=None,
            answer_correct=None,
            state=EventStates.Initialized
        )

        result = self.waypoint_event_repository.add(event)

        return result

    def finish_event(self, event_id, user_id, answer_id):
        event = self.waypoint_event_repository.get_by_id(event_id)

        if event is None:
            return None

        answer_correct = answer_id == event.question.correct_answer_id

        event.state = EventStates.Finished
        event.answer_correct = answer_correct

        result = self.waypoint_event_repository.update(event)

        return result

    def validate_event_question(self, event_id, question_id, user_id):
        event = self.waypoint_event_repository.get_by_id(event_id)
        time_for_answer = 65

        if event is None:
            return False

        if event.question is None:
            return False

        if event.question.id != question_id:
            return False

        if event.user.id != user_id:
            return False

        current_timestamp = datetime.datetime.now().timestamp()
        if event.timestamp < current_timestamp - time_for_answer:
            return False

        return True

    def get_events_for_user(self, user_id):
        events = self.waypoint_event_repository.get_waypoint_events_for_user(user_id)
        return [
            {
                "id": event.id,
                "waypoint_id": event.waypoint.id,
                "state": event.state,
                "answer_correct": event.answer_correct
            } for event in events
        ]
