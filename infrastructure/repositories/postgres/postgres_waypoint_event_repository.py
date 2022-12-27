from injector import inject
from sqlalchemy.exc import SQLAlchemyError

from domain.enums.event_states import EventStates
from domain.enums.roles import Roles
from domain.models.question import Question
from domain.models.user import User
from domain.models.waypoint import Waypoint
from domain.models.waypoint_event import WaypointEvent
from domain.repositories.waypoint_event_repository import WaypointEventRepository
from infrastructure.database.database_provider import DatabaseProvider

from infrastructure.models.waypoint_event import WaypointEvent as WaypointEventModel
from infrastructure.models.user import User as UserModel
from infrastructure.models.question import Question as QuestionModel
from infrastructure.models.waypoint import Waypoint as WaypointModel


class PostgresWaypointEventRepository(WaypointEventRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db = db_provider.get_db()

    def event_for_waypoint_exists(self, user_id, waypoint_id) -> bool:
        existing_event = self.db.query(WaypointEventModel)\
            .filter_by(user_id=user_id, waypoint_id=waypoint_id)\
            .one_or_none()

        if existing_event is not None:
            return True

        return False

    def get_waypoint_events_for_user(self, user_id) -> list[WaypointEvent]:
        events = self.db.query(WaypointEventModel).filter_by(user_id=user_id)

        return [self._create_event(event) for event in events]

    def get_by_id(self, event_id) -> WaypointEvent or None:
        event = self.db.query(WaypointEventModel).filter_by(id=event_id).one_or_none()

        if event is None:
            return None

        return self._create_event(event)

    def add(self, event: WaypointEvent) -> WaypointEvent or None:
        waypoint = self.db.query(WaypointModel).filter_by(id=event.waypoint.id).one_or_none()
        user = self.db.query(UserModel).filter_by(id=event.user.id).one_or_none()

        question = self.db.query(QuestionModel).filter_by(id=event.question.id).one_or_none()\
            if event.question is not None else None

        event_model = WaypointEventModel(
            timestamp=event.timestamp,
            waypoint=waypoint,
            user=user,
            question=question,
            answer_correct=event.answer_correct,
            state=event.state,
        )

        result = None

        try:
            self.db.add(event_model)
        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
            self.db.refresh(event_model)

            result = self._create_event(event_model)
        finally:
            self.db.close()

        return result

    def update(self, event: WaypointEvent) -> WaypointEvent or None:
        waypoint_event: WaypointEventModel = self.db.query(WaypointEventModel).filter_by(id=event.id).one_or_none()
        waypoint = self.db.query(WaypointModel).filter_by(id=event.waypoint.id).one_or_none()
        user = self.db.query(UserModel).filter_by(id=event.user.id).one_or_none()

        question = self.db.query(QuestionModel).filter_by(id=event.question.id).one_or_none() \
            if event.question is not None else None


        if waypoint_event is None:
            return None

        waypoint_event.timestamp = event.timestamp
        waypoint_event.question = question
        waypoint_event.user = user
        waypoint_event.waypoint = waypoint
        waypoint_event.state = event.state
        waypoint_event.answer_correct = event.answer_correct

        result = None

        try:
            self.db.add(waypoint_event)
        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
            self.db.refresh(waypoint_event)

            result = self._create_event(waypoint_event)
        finally:
            self.db.close()

        return result

    def _create_event(self, event) -> WaypointEvent:
        return WaypointEvent(
            id=event.id,
            timestamp=event.timestamp,
            user=User(
                id=event.user.id,
                username=event.user.username,
                password=event.user.password,
                role=Roles(event.user.role),
                question_answers=[]
            ),
            waypoint=Waypoint(
                id=event.waypoint.id,
                title=event.waypoint.title,
                description=event.waypoint.description,
                coordinateX=event.waypoint.coordinateX,
                coordinateY=event.waypoint.coordinateY
            ),
            question=Question(
                id=event.question.id,
                contents=event.question.contents,
                answers=[],
                correct_answer_id=event.question.correct_answer_id
            ) if event.question is not None else None,
            answer_correct=event.answer_correct,
            state=EventStates(event.state)
        )
