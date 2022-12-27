import uuid

import bcrypt
from injector import inject
from sqlalchemy.exc import SQLAlchemyError

from domain.enums.roles import Roles
from infrastructure.models.user import User as UserModel
from domain.models.user import User
from domain.repositories.users_repository import UsersRepository
from infrastructure.database.database_provider import DatabaseProvider


class PostgresUsersRepository(UsersRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db = db_provider.get_db()

    def add(self, username: str, password: str) -> User or None:
        salt = bcrypt.gensalt()
        user_model = UserModel(
            username=username,
            password=bcrypt.hashpw(password.encode("utf-8"), salt),
            role=Roles.User
        )

        result = None

        try:
            self.db.add(user_model)
        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
            self.db.refresh(user_model)

            result = User(
                id=user_model.id,
                username=user_model.username,
                password=user_model.password,
                role=Roles(user_model.role),
                question_answers=[]
            )
        finally:
            self.db.close()

        return result

    def get_by_name(self, username: str) -> User or None:
        result = self.db.query(UserModel).filter_by(username=username).one_or_none()

        if result is None:
            return None

        user = User(
            id=result.id,
            username=result.username,
            password=result.password,
            role=Roles(result.role),
            question_answers=result.question_answers
        )

        return user

    def get_by_id(self, user_id: str) -> User or None:
        result = self.db.query(UserModel).filter_by(id=user_id).one_or_none()

        if result is None:
            return None

        user = User(
            id=result.id,
            username=result.username,
            password=result.password,
            role=Roles(result.role),
            question_answers=result.question_answers
        )

        return user
