from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from application.extensions.database import Base
from application.utils.uuid_generator import generate_uuid

from infrastructure.models.question import Question


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id = Column(String, primary_key=True, default=generate_uuid)
    question_id = Column(String, ForeignKey("questions.id"))
    question = relationship("Question")
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="question_answers")
    answer_id = Column(String, ForeignKey("answers.id"))
    answer = relationship("Answer")

