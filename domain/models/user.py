from dataclasses import dataclass
from domain.enums.roles import Roles
from domain.models.question_answer import QuestionAnswer


@dataclass
class User:
    id: str
    username: str
    password: bytes
    role: Roles
    question_answers: list[QuestionAnswer]
