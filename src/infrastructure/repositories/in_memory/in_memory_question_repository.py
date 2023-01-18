import uuid

from injector import inject

from src.domain.models.question import Question
from src.domain.repositories.question_repository import QuestionRepository
from src.infrastructure.database.database_provider import DatabaseProvider


class InMemoryQuestionRepository(QuestionRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db_provider = db_provider

    def get_all(self):
        db = self.db_provider.get_db()

        if db is None or db.get("questions") is None:
            return []

        return [
            Question(question_id, **question_data)
            for question_id, question_data in db["questions"].items()
        ]

    def get_by_id(self, question_id):
        db = self.db_provider.get_db()

        if db is None or db.get("questions") is None:
            return None

        question_data = db["questions"].get(question_id)

        if question_data is None:
            return None

        return Question(question_id, **question_data)

    def add(self, question):
        db = self.db_provider.get_db()

        if db is None or db.get("questions") is None:
            return None

        question_id = str(uuid.uuid4())

        question = {
            "contents": question.get("contents"),
            "answers": question.get("answers"),
            "correct_answer_id": question.get("correct_answer_id"),
        }

        db["questions"][question_id] = question

        return question

    def update(self, question, question_id):
        db = self.db_provider.get_db()

        if db is None or db.get("questions") is None:
            return None

        if question_id is None:
            return None

        db_question = db["questions"].get(question_id)

        if db_question is None:
            return None

        db_question["contents"] = question.get("contents")
        db_question["answers"] = question.get("answers")
        db_question["correct_answer_id"] = question.get("correct_answer_id")

        db["questions"][question_id] = db_question

        return db_question

    def delete(self, question_id):
        db = self.db_provider.get_db()

        if db is None or db.get("questions") is None:
            return

        db_question = db["questions"].get(question_id)

        if db_question is None:
            return

        del db["questions"][question_id]
