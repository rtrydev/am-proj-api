import uuid

from injector import inject
from sqlalchemy.exc import SQLAlchemyError

from infrastructure.models.question import Question as QuestionModel
from infrastructure.models.answer import Answer as AnswerModel

from domain.models.question import Question
from domain.repositories.question_repository import QuestionRepository
from infrastructure.database.database_provider import DatabaseProvider


class PostgresQuestionRepository(QuestionRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db = db_provider.get_db()

    def get_all(self) -> list[Question]:
        result = self.db.query(QuestionModel)

        return [
            Question(
                id=item.id,
                contents=item.contents,
                answers=item.answers,
                correct_answer_id=item.correct_answer_id
            ) for item in result
        ]

    def get_by_id(self, question_id) -> Question or None:
        result = self.db.query(QuestionModel).filter_by(id=question_id).one_or_none()

        if result is None:
            return None

        question = Question(
            id=result.id,
            contents=result.contents,
            answers=result.answers,
            correct_answer_id=result.correct_answer_id
        )

        return question

    def add(self, question) -> Question or None:
        answers = question.get("answers")

        answer_ids = {
            answer.get("answer_id"): str(uuid.uuid4())
            for answer in answers
        }

        question_model = QuestionModel(
            contents=question.get("contents"),
            correct_answer_id=answer_ids[question.get("correct_answer_id")]
        )

        answer_models = [
            AnswerModel(
                id=answer_ids[answer.get("answer_id")],
                text=answer.get("text"),
                question=question_model
            ) for answer in answers
        ]

        result = None

        try:
            self.db.add(question_model)

            for answer in answer_models:
                self.db.add(answer)

        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
            self.db.refresh(question_model)

            result = Question(
                id=question_model.id,
                contents=question_model.contents,
                answers=question_model.answers,
                correct_answer_id=question_model.correct_answer_id
            )
        finally:
            self.db.close()

        return result

    def update(self, question, question_id) -> Question or None:
        question_model = self.db.query(QuestionModel).filter_by(id=question_id).one_or_none()

        if question_model is None:
            return None

        question_model.contents = question.get("contents")
        question_model.correct_answer_id = question.get("correct_answer_id")

        result = None

        try:
            self.db.add(question_model)
        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
            self.db.refresh(question_model)

            result = Question(
                id=question_model.id,
                contents=question_model.contents,
                answers=question_model.answers,
                correct_answer_id=question_model.correct_answer_id
            )
        finally:
            self.db.close()

        return result

    def delete(self, question_id):
        question_model = self.db.query(QuestionModel).filter_by(id=question_id).one_or_none()

        if question_model is None:
            return

        try:
            self.db.delete(question_model)
        except SQLAlchemyError:
            self.db.rollback()
        else:
            self.db.commit()
        finally:
            self.db.close()
