from abc import ABC, abstractmethod


class AuthService(ABC):
    @abstractmethod
    def generate_token(self, payload: dict):
        pass
