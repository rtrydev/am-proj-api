import uuid

import bcrypt
from injector import inject

from src.domain.enums.roles import Roles
from src.domain.models.user import User
from src.domain.repositories.users_repository import UsersRepository
from src.infrastructure.database.database_provider import DatabaseProvider


class InMemoryUsersRepository(UsersRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db_provider = db_provider

    def add(self, username: str, password: str) -> User or None:
        db = self.db_provider.get_db()

        if db is None or db.get("users") is None:
            return None

        if self.get_by_name(username) is not None:
            return None

        user_id = str(uuid.uuid4())

        salt = bcrypt.gensalt()
        user = {
            "username": username,
            "password": bcrypt.hashpw(password.encode("utf-8"), salt),
            "role": Roles.User
        }

        db["users"][user_id] = user

        return user

    def get_by_name(self, username: str) -> User or None:
        db = self.db_provider.get_db()

        if db is None or db.get("users") is None:
            return None

        user = next(
            (User(user_id, **user)
             for user_id, user in db["users"].items()
             if user["username"] == username),
            None
        )

        return user

    def get_by_id(self, user_id: str) -> User or None:
        db = self.db_provider.get_db()

        if db is None or db.get("users") is None:
            return None

        return User(user_id, **db["users"].get(user_id))
