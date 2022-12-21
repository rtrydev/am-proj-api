import uuid

from injector import inject

from domain.repositories.question_answers_repository import QuestionAnswersRepository
from infrastructure.database.database_provider import DatabaseProvider


class InMemoryQuestionAnswersRepository(QuestionAnswersRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db_provider = db_provider

    def get_answers_for_user(self, user_id):
        db = self.db_provider.get_db()

        if db is None or db.get("question_answers") is None:
            return []

        all_answers = db["question_answers"]

        answers_for_user = [
            {
                "id": key,
                "user_id": answer.get("user_id"),
                "question_id": answer.get("question_id"),
                "answer_id": answer.get("answer_id")
            }
            for key, answer in all_answers.items()
            if answer.get("user_id") == user_id
        ]

        return answers_for_user

    def add(self, question_id, answer_id, user_id):
        db = self.db_provider.get_db()

        if db is None or db.get("question_answers") is None:
            return None

        if db["questions"].get(question_id) is None:
            return None

        if not any(answer
                   for answer in db["questions"][question_id].get("answers")
                   if answer.get("answer_id") == answer_id
                   ):
            return None

        if any(key
               for key, answer in db["question_answers"].items()
               if answer.get("user_id") == user_id and answer.get("question_id") == question_id
               ):
            return None

        entry_id = str(uuid.uuid4())

        answer = {
            "user_id": user_id,
            "question_id": question_id,
            "answer_id": answer_id
        }

        db["question_answers"][entry_id] = answer

        return answer
