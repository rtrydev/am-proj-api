from abc import ABC, abstractmethod

from src.domain.models.question_answer import QuestionAnswer


class QuestionAnswersRepository(ABC):
    @abstractmethod
    def get_answers_for_user(self, user_id: str) -> list[QuestionAnswer]:
        pass

    @abstractmethod
    def add(self, question_id, answer_id, user_id) -> QuestionAnswer or None:
        pass
