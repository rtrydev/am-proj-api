import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from application.extensions.database import Base


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    question_id = Column(String, ForeignKey("questions.id"))
    question = relationship("Question")
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="question_answers")
    text = Column(String)
