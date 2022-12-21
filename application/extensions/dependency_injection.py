import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import singleton

from application.extensions.database import configure_db
from domain.repositories.question_answers_repository import QuestionAnswersRepository
from domain.repositories.question_repository import QuestionRepository
from domain.repositories.users_repository import UsersRepository
from domain.repositories.waypoint_repository import WaypointRepository
from domain.services.auth_service import AuthService
from infrastructure.database.database_provider import DatabaseProvider
from infrastructure.database.in_memory.in_memory_database_provider import InMemoryDatabaseProvider
from infrastructure.repositories.in_memory.in_memory_question_answers_repository import InMemoryQuestionAnswersRepository
from infrastructure.repositories.in_memory.in_memory_question_repository import InMemoryQuestionRepository
from infrastructure.repositories.in_memory.in_memory_users_repository import InMemoryUsersRepository
from infrastructure.repositories.in_memory.in_memory_waypoint_repository import InMemoryWaypointRepository
from infrastructure.services.jwt_service import JwtService


def configure(binder):
    use_persistent_db = os.environ.get("PERSISTENT_DB") is True

    if not use_persistent_db:
        _bind_inmemory_db(binder)
    else:
        _bind_persistent_db(binder)

    binder.bind(AuthService, to=JwtService, scope=singleton)


def _bind_inmemory_db(binder):
    binder.bind(DatabaseProvider, to=InMemoryDatabaseProvider, scope=singleton)
    binder.bind(WaypointRepository, to=InMemoryWaypointRepository, scope=singleton)
    binder.bind(UsersRepository, to=InMemoryUsersRepository, scope=singleton)
    binder.bind(QuestionRepository, to=InMemoryQuestionRepository, scope=singleton)
    binder.bind(QuestionAnswersRepository, to=InMemoryQuestionAnswersRepository, scope=singleton)


def _bind_persistent_db(binder):
    app = binder.injector.get(Flask)
    db = configure_db(app)

    binder.bind(SQLAlchemy, to=db, scope=singleton)



