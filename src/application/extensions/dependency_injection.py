import os

from injector import singleton

from src.application.services.waypoint_event_service import WaypointEventService
from src.domain.repositories.question_answers_repository import QuestionAnswersRepository
from src.domain.repositories.question_repository import QuestionRepository
from src.domain.repositories.users_repository import UsersRepository
from src.domain.repositories.waypoint_event_repository import WaypointEventRepository
from src.domain.repositories.waypoint_repository import WaypointRepository
from src.domain.services.auth_service import AuthService
from src.domain.services.waypoint_event_service import WaypointEventServiceInterface
from src.infrastructure.database.database_provider import DatabaseProvider
from src.infrastructure.database.in_memory.in_memory_database_provider import InMemoryDatabaseProvider
from src.infrastructure.database.postgres.postgres_database_provider import PostgresDatabaseProvider
from src.infrastructure.repositories.in_memory.in_memory_question_answers_repository import InMemoryQuestionAnswersRepository
from src.infrastructure.repositories.in_memory.in_memory_question_repository import InMemoryQuestionRepository
from src.infrastructure.repositories.in_memory.in_memory_users_repository import InMemoryUsersRepository
from src.infrastructure.repositories.in_memory.in_memory_waypoint_event_repository import InMemoryWaypointEventRepository
from src.infrastructure.repositories.in_memory.in_memory_waypoint_repository import InMemoryWaypointRepository
from src.infrastructure.repositories.postgres.postgres_question_answers_repository import PostgresQuestionAnswersRepository
from src.infrastructure.repositories.postgres.postgres_question_repository import PostgresQuestionRepository
from src.infrastructure.repositories.postgres.postgres_users_repository import PostgresUsersRepository
from src.infrastructure.repositories.postgres.postgres_waypoint_event_repository import PostgresWaypointEventRepository
from src.infrastructure.repositories.postgres.postgres_waypoint_repository import PostgresWaypointRepository
from src.application.services.jwt_service import JwtService


def configure(binder):
    use_persistent_db = os.environ.get("PERSISTENT_DB") == "true"

    if not use_persistent_db:
        _bind_in_memory_db(binder)
    else:
        _bind_persistent_db(binder)

    binder.bind(AuthService, to=JwtService, scope=singleton)
    binder.bind(WaypointEventServiceInterface, to=WaypointEventService, scope=singleton)


def _bind_in_memory_db(binder):
    print("Initializing in memory database")
    binder.bind(DatabaseProvider, to=InMemoryDatabaseProvider, scope=singleton)
    binder.bind(WaypointRepository, to=InMemoryWaypointRepository, scope=singleton)
    binder.bind(UsersRepository, to=InMemoryUsersRepository, scope=singleton)
    binder.bind(QuestionRepository, to=InMemoryQuestionRepository, scope=singleton)
    binder.bind(QuestionAnswersRepository, to=InMemoryQuestionAnswersRepository, scope=singleton)
    binder.bind(WaypointEventRepository, to=InMemoryWaypointEventRepository, scope=singleton)


def _bind_persistent_db(binder):
    print("Initializing in persistent database")
    binder.bind(DatabaseProvider, to=PostgresDatabaseProvider, scope=singleton)
    binder.bind(WaypointRepository, to=PostgresWaypointRepository, scope=singleton)
    binder.bind(UsersRepository, to=PostgresUsersRepository, scope=singleton)
    binder.bind(QuestionRepository, to=PostgresQuestionRepository, scope=singleton)
    binder.bind(QuestionAnswersRepository, to=PostgresQuestionAnswersRepository, scope=singleton)
    binder.bind(WaypointEventRepository, to=PostgresWaypointEventRepository, scope=singleton)
