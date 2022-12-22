import os

from injector import singleton

from application.services.waypoint_event_service import WaypointEventService
from domain.repositories.question_answers_repository import QuestionAnswersRepository
from domain.repositories.question_repository import QuestionRepository
from domain.repositories.users_repository import UsersRepository
from domain.repositories.waypoint_event_repository import WaypointEventRepository
from domain.repositories.waypoint_repository import WaypointRepository
from domain.services.auth_service import AuthService
from domain.services.waypoint_event_service import WaypointEventServiceInterface
from infrastructure.database.database_provider import DatabaseProvider
from infrastructure.database.in_memory.in_memory_database_provider import InMemoryDatabaseProvider
from infrastructure.database.postgres.postgres_database_provider import PostgresDatabaseProvider
from infrastructure.repositories.in_memory.in_memory_question_answers_repository import InMemoryQuestionAnswersRepository
from infrastructure.repositories.in_memory.in_memory_question_repository import InMemoryQuestionRepository
from infrastructure.repositories.in_memory.in_memory_users_repository import InMemoryUsersRepository
from infrastructure.repositories.in_memory.in_memory_waypoint_event_repository import InMemoryWaypointEventRepository
from infrastructure.repositories.in_memory.in_memory_waypoint_repository import InMemoryWaypointRepository
from infrastructure.repositories.postgres.postgres_waypoint_repository import PostgresWaypointRepository
from application.services.jwt_service import JwtService


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



