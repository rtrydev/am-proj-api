from dataclasses import dataclass


@dataclass
class QuestionAnswer:
    question_id: str
    answer_id: str
    text: str
