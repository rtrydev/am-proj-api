from dataclasses import dataclass

from domain.models.question_answer import QuestionAnswer


@dataclass
class Question:
    id: str
    contents: str
    answers: list[QuestionAnswer]
    correct_answer_id: str
