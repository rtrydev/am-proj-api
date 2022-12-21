from injector import inject

from domain.models.user import User
from domain.repositories.users_repository import UsersRepository
from infrastructure.database.database_provider import DatabaseProvider


class PostgresUsersRepository(UsersRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db_provider = db_provider

    def add(self, username: str, password: str) -> User or None:
        pass

    def get_by_name(self, username: str) -> User or None:
        pass

    def get_by_id(self, user_id: str) -> User or None:
        pass
