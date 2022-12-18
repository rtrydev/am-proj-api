from abc import ABC, abstractmethod


class DatabaseProvider(ABC):
    @abstractmethod
    def get_db(self):
        pass
