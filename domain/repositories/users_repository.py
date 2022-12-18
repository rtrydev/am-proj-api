from abc import ABC, abstractmethod

from domain.models.user import User


class UsersRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User or None:
        pass

    @abstractmethod
    def get_by_credentials(self, username: str, password: str) -> User or None:
        pass
