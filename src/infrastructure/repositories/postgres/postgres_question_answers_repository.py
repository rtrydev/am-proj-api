from injector import inject
from sqlalchemy.exc import SQLAlchemyError

from src.domain.models.question_answer import QuestionAnswer
from src.domain.repositories.question_answers_repository import QuestionAnswersRepository
from src.infrastructure.database.database_provider import DatabaseProvider

from src.infrastructure.models.question_answer import QuestionAnswer as QuestionAnswerModel
from src.infrastructure.models.question import Question as QuestionModel


class PostgresQuestionAnswersRepository(QuestionAnswersRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db = db_provider.get_db()

    def get_answers_for_user(self, user_id: str) -> list[QuestionAnswer]:
        result = self.db.query(QuestionAnswerModel).filter_by(user_id=user_id)

        if result is None:
            return []

        question_answers = [
            QuestionAnswer(
                id=answer.id,
                question_id=answer.question_id,
                answer_id=answer.answer_id,
                user_id=answer.user_id
            ) for answer in result
        ]

        return question_answers

    def add(self, question_id, answer_id, user_id) -> QuestionAnswer or None:
        question: QuestionModel = self.db.query(QuestionModel).filter_by(id=question_id).one_or_none()

        if question is None:
            return None

        if not any(answer
                   for answer in question.answers
                   if answer.id == answer_id
                   ):
            return None

        existing_question_answer = self.db.query(QuestionAnswerModel)\
            .filter_by(user_id=user_id, question_id=question_id)\
            .one_or_none()

        if existing_question_answer is not None:
            return None

        question_answer = QuestionAnswerModel(
            user_id=user_id,
            question_id=question_id,
            answer_id=answer_id
        )

        result = None

        try:
            self.db.add(question_answer)
        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
            self.db.refresh(question_answer)

            result = QuestionAnswer(
                id=question_answer.id,
                user_id=question_answer.user_id,
                question_id=question_answer.question_id,
                answer_id=question_answer.answer_id,
            )
        finally:
            self.db.close()

        return result
