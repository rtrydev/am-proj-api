from injector import singleton

from domain.repositories.users_repository import UsersRepository
from domain.repositories.waypoint_repository import WaypointRepository
from domain.services.auth_service import AuthService
from infrastructure.database.database_provider import DatabaseProvider
from infrastructure.database.inmemory_database_provider import InMemoryDatabaseProvider
from infrastructure.repositories.inmemory_users_repository import InMemoryUsersRepository
from infrastructure.repositories.inmemory_waypoint_repository import InMemoryWaypointRepository
from infrastructure.services.jwt_service import JwtService


def configure(binder):
    binder.bind(DatabaseProvider, to=InMemoryDatabaseProvider, scope=singleton)
    binder.bind(WaypointRepository, to=InMemoryWaypointRepository, scope=singleton)
    binder.bind(UsersRepository, to=InMemoryUsersRepository, scope=singleton)
    binder.bind(AuthService, to=JwtService, scope=singleton)
