from abc import ABC, abstractmethod

from domain.models.user import User


class UsersRepository(ABC):
    @abstractmethod
    def add(self, username: str, password: str) -> User or None:
        pass

    @abstractmethod
    def get_by_name(self, username: str) -> User or None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> User or None:
        pass
