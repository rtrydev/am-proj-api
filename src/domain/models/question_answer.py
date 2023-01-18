from dataclasses import dataclass


@dataclass
class QuestionAnswer:
    id: str
    question_id: str
    answer_id: str
    user_id: str
