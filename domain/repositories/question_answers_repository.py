from abc import ABC, abstractmethod


class QuestionAnswersRepository(ABC):
    @abstractmethod
    def get_answers_for_user(self, user_id):
        pass

    @abstractmethod
    def add(self, question_id, answer_id, user_id):
        pass
