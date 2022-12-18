from abc import ABC, abstractmethod


class QuestionRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, question_id):
        pass

    @abstractmethod
    def add(self, question):
        pass

    @abstractmethod
    def update(self, question, question_id):
        pass

    @abstractmethod
    def delete(self, question_id):
        pass
