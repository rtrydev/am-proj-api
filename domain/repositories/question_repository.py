from abc import ABC, abstractmethod

from domain.models.question import Question


class QuestionRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Question]:
        pass

    @abstractmethod
    def get_by_id(self, question_id) -> Question or None:
        pass

    @abstractmethod
    def add(self, question) -> Question or None:
        pass

    @abstractmethod
    def update(self, question, question_id) -> Question or None:
        pass

    @abstractmethod
    def delete(self, question_id):
        pass
