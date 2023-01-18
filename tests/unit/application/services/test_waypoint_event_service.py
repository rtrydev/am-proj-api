import unittest
from unittest.mock import Mock, MagicMock, call

import pytest

from src.application.services.waypoint_event_service import WaypointEventService
from src.domain.enums.event_states import EventStates
from src.domain.enums.roles import Roles
from src.domain.models.answer import Answer
from src.domain.models.question import Question
from src.domain.models.user import User
from src.domain.models.waypoint import Waypoint
from src.domain.models.waypoint_event import WaypointEvent


class TestWaypointEventService(unittest.TestCase):
    def setUp(self):
        self.waypoint_event_repository = Mock()
        self.users_repository = Mock()
        self.question_repository = Mock()
        self.waypoint_repository = Mock()

        self.waypoint_event_service = WaypointEventService(
            self.waypoint_event_repository,
            self.users_repository,
            self.question_repository,
            self.waypoint_repository
        )

        self.expected_questions = [
            Question(
                id="test",
                answers=[
                    Answer(
                        id="test1",
                        text="a1"
                    ),
                    Answer(
                        id="test2",
                        text="a2"
                    ),
                    Answer(
                        id="test3",
                        text="a3"
                    )
                ],
                contents="test",
                correct_answer_id="test1"
            ),
            Question(
                id="test2",
                answers=[
                    Answer(
                        id="test1",
                        text="a1"
                    ),
                    Answer(
                        id="test2",
                        text="a2"
                    ),
                    Answer(
                        id="test3",
                        text="a3"
                    )
                ],
                contents="test",
                correct_answer_id="test1"
            )
        ]

        self.question_repository.get_all = MagicMock(
            return_value=self.expected_questions
        )

        self.waypoint_event_repository.update = Mock()

    @pytest.mark.unit
    def test_get_random_question__success(self):
        self.waypoint_event_repository.get_by_id = MagicMock(
            return_value=WaypointEvent(
                id="test",
                timestamp=123123,
                waypoint=Waypoint(
                    id="test",
                    coordinateX=123.312,
                    coordinateY=33.123,
                    description="test",
                    title="way1"
                ),
                state=EventStates.Initialized,
                answer_correct=None,
                question=None,
                user=User(
                    id="user1",
                    username="usertest",
                    password=None,
                    question_answers=[],
                    role=Roles.User
                )
            )
        )

        random_question = self.waypoint_event_service.get_random_question_for_event(
            event_id="test",
            user_id="user1"
        )

        assert random_question in self.expected_questions
        assert self.waypoint_event_repository.update.has_calls(
            call(
                WaypointEvent(
                    id="test",
                    timestamp=123123,
                    waypoint=Waypoint(
                        id="test",
                        coordinateX=123.312,
                        coordinateY=33.123,
                        description="test",
                        title="way1"
                    ),
                    state=EventStates.QuestionReceived,
                    answer_correct=None,
                    question=None,
                    user=User(
                        id="user1",
                        username="usertest",
                        password=None,
                        question_answers=[],
                        role=Roles.User
                    )
                )
            ),
            call(
                WaypointEvent(
                    id="test",
                    timestamp=123123,
                    waypoint=Waypoint(
                        id="test",
                        coordinateX=123.312,
                        coordinateY=33.123,
                        description="test",
                        title="way1"
                    ),
                    state=EventStates.QuestionReceived,
                    answer_correct=None,
                    question=random_question,
                    user=User(
                        id="user1",
                        username="usertest",
                        password=None,
                        question_answers=[],
                        role=Roles.User
                    )
                )
            )
        )

    @pytest.mark.unit
    def test_get_random_question__no_event__fail(self):
        self.waypoint_event_repository.get_by_id = MagicMock(
            return_value=None
        )

        random_question = self.waypoint_event_service.get_random_question_for_event(
            event_id="test",
            user_id="user1"
        )

        assert random_question is None

    @pytest.mark.unit
    def test_get_random_question__another_user__fail(self):
        self.waypoint_event_repository.get_by_id = MagicMock(
            return_value=WaypointEvent(
                id="test",
                timestamp=123123,
                waypoint=Waypoint(
                    id="test",
                    coordinateX=123.312,
                    coordinateY=33.123,
                    description="test",
                    title="way1"
                ),
                state=EventStates.Initialized,
                answer_correct=None,
                question=None,
                user=User(
                    id="user2",
                    username="usertest",
                    password=None,
                    question_answers=[],
                    role=Roles.User
                )
            )
        )

        random_question = self.waypoint_event_service.get_random_question_for_event(
            event_id="test",
            user_id="user1"
        )

        assert random_question is None

    @pytest.mark.unit
    def test_get_random_question__wrong_state__fail(self):
        self.waypoint_event_repository.get_by_id = MagicMock(
            return_value=WaypointEvent(
                id="test",
                timestamp=123123,
                waypoint=Waypoint(
                    id="test",
                    coordinateX=123.312,
                    coordinateY=33.123,
                    description="test",
                    title="way1"
                ),
                state=EventStates.QuestionReceived,
                answer_correct=None,
                question=None,
                user=User(
                    id="user1",
                    username="usertest",
                    password=None,
                    question_answers=[],
                    role=Roles.User
                )
            )
        )

        random_question = self.waypoint_event_service.get_random_question_for_event(
            event_id="test",
            user_id="user1"
        )

        assert random_question is None

    @pytest.mark.unit
    def test_get_random_question__failed_state_update__fail(self):
        self.waypoint_event_repository.get_by_id = MagicMock(
            return_value=WaypointEvent(
                id="test",
                timestamp=123123,
                waypoint=Waypoint(
                    id="test",
                    coordinateX=123.312,
                    coordinateY=33.123,
                    description="test",
                    title="way1"
                ),
                state=EventStates.Initialized,
                answer_correct=None,
                question=None,
                user=User(
                    id="user1",
                    username="usertest",
                    password=None,
                    question_answers=[],
                    role=Roles.User
                )
            )
        )

        self.waypoint_event_repository.update = MagicMock(
            return_value=None
        )

        random_question = self.waypoint_event_service.get_random_question_for_event(
            event_id="test",
            user_id="user1"
        )

        assert random_question is None

    @pytest.mark.unit
    def test_init_waypoint_event__success(self):
        self.users_repository.get_by_id = MagicMock(
            return_value=User(
                id="testuser",
                username="test",
                password=None,
                question_answers=[],
                role=Roles.User
            )
        )

        self.waypoint_repository.get_by_id = MagicMock(
            return_value=Waypoint(
                id="test",
                coordinateX=123.312,
                coordinateY=33.123,
                description="test",
                title="way1"
            )
        )

        self.waypoint_event_repository.event_for_waypoint_exists = MagicMock(
            return_value=False
        )

        self.waypoint_event_repository.add = Mock()

        event_init_result = self.waypoint_event_service.init_waypoint_event(
            "test",
            "testuser"
        )

        assert event_init_result is not None
        assert self.waypoint_event_repository.add.called

    @pytest.mark.unit
    def test_init_waypoint_event__missing_user__fail(self):
        self.users_repository.get_by_id = MagicMock(
            return_value=None
        )

        self.waypoint_repository.get_by_id = MagicMock(
            return_value=Waypoint(
                id="test",
                coordinateX=123.312,
                coordinateY=33.123,
                description="test",
                title="way1"
            )
        )

        self.waypoint_event_repository.event_for_waypoint_exists = MagicMock(
            return_value=False
        )

        self.waypoint_event_repository.add = Mock()

        event_init_result = self.waypoint_event_service.init_waypoint_event(
            "test",
            "testuser"
        )

        assert event_init_result is None

    @pytest.mark.unit
    def test_init_waypoint_event__missing_waypoint__fail(self):
        self.users_repository.get_by_id = MagicMock(
            return_value=User(
                id="testuser",
                username="test",
                password=None,
                question_answers=[],
                role=Roles.User
            )
        )

        self.waypoint_repository.get_by_id = MagicMock(
            return_value=None
        )

        self.waypoint_event_repository.event_for_waypoint_exists = MagicMock(
            return_value=False
        )

        self.waypoint_event_repository.add = Mock()

        event_init_result = self.waypoint_event_service.init_waypoint_event(
            "test",
            "testuser"
        )

        assert event_init_result is None

    @pytest.mark.unit
    def test_init_waypoint_event__event_exists__fail(self):
        self.users_repository.get_by_id = MagicMock(
            return_value=User(
                id="testuser",
                username="test",
                password=None,
                question_answers=[],
                role=Roles.User
            )
        )

        self.waypoint_repository.get_by_id = MagicMock(
            return_value=Waypoint(
                id="test",
                coordinateX=123.312,
                coordinateY=33.123,
                description="test",
                title="way1"
            )
        )

        self.waypoint_event_repository.event_for_waypoint_exists = MagicMock(
            return_value=True
        )

        self.waypoint_event_repository.add = Mock()

        event_init_result = self.waypoint_event_service.init_waypoint_event(
            "test",
            "testuser"
        )

        assert event_init_result is None

    @pytest.mark.unit
    def test_finish_event__success(self):
        self.waypoint_event_repository.get_by_id = MagicMock(
            return_value=WaypointEvent(
                id="test",
                timestamp=123123,
                waypoint=Waypoint(
                    id="test",
                    coordinateX=123.312,
                    coordinateY=33.123,
                    description="test",
                    title="way1"
                ),
                state=EventStates.QuestionReceived,
                answer_correct=None,
                question=Question(
                    id="test",
                    answers=[
                        Answer(
                            id="test1",
                            text="a1"
                        ),
                        Answer(
                            id="test2",
                            text="a2"
                        ),
                        Answer(
                            id="test3",
                            text="a3"
                        )
                    ],
                    contents="test",
                    correct_answer_id="test1"
                ),
                user=User(
                    id="user1",
                    username="usertest",
                    password=None,
                    question_answers=[],
                    role=Roles.User
                )
            )
        )

        self.waypoint_event_repository.update = Mock()

        result = self.waypoint_event_service.finish_event(
            "test",
            "usertest",
            "test2"
        )

        assert result is not None
        self.waypoint_event_repository.update.assert_has_calls(
            [call(
                WaypointEvent(
                    id="test",
                    timestamp=123123,
                    waypoint=Waypoint(
                        id="test",
                        coordinateX=123.312,
                        coordinateY=33.123,
                        description="test",
                        title="way1"
                    ),
                    state=EventStates.Finished,
                    answer_correct=False,
                    question=Question(
                        id="test",
                        answers=[
                            Answer(
                                id="test1",
                                text="a1"
                            ),
                            Answer(
                                id="test2",
                                text="a2"
                            ),
                            Answer(
                                id="test3",
                                text="a3"
                            )
                        ],
                        contents="test",
                        correct_answer_id="test1"
                    ),
                    user=User(
                        id="user1",
                        username="usertest",
                        password=None,
                        question_answers=[],
                        role=Roles.User
                    )
                )
            )]
        )

    @pytest.mark.unit
    def test_finish_event__no_event__fail(self):
        self.waypoint_event_repository.get_by_id = MagicMock(
            return_value=None
        )
        self.waypoint_event_repository.update = Mock()

        result = self.waypoint_event_service.finish_event(
            "test",
            "usertest",
            "test1"
        )

        assert result is None
