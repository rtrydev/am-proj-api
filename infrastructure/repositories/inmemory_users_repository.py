from injector import inject

from domain.models.user import User
from domain.repositories.users_repository import UsersRepository
from infrastructure.database.database_provider import DatabaseProvider


class InMemoryUsersRepository(UsersRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db_provider = db_provider

    def add(self, user: User) -> User or None:
        pass

    def get_by_credentials(self, username: str, password: str) -> User or None:
        db = self.db_provider.get_db()

        if db is None or db.get("users") is None:
            return None

        user = next(
            (User(user_id, **user)
             for user_id, user in db["users"].items()
             if user["username"] == username and user["password"] == password)
        )

        return user
