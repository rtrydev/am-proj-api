from injector import singleton

from domain.repositories.waypoint_repository import WaypointRepository
from infrastructure.database.database_provider import DatabaseProvider
from infrastructure.database.inmemory_database_provider import InMemoryDatabaseProvider
from infrastructure.repositories.inmemory_waypoint_repository import InMemoryWaypointRepository


def configure(binder):
    binder.bind(DatabaseProvider, to=InMemoryDatabaseProvider, scope=singleton)
    binder.bind(WaypointRepository, to=InMemoryWaypointRepository, scope=singleton)
