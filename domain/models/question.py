from dataclasses import dataclass

from domain.models.answer import Answer


@dataclass
class Question:
    id: str
    contents: str
    answers: list[Answer]
    correct_answer_id: str
