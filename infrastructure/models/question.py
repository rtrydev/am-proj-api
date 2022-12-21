import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from application.extensions.database import Base


class Question(Base):
    __tablename__ = "questions"

    def __init__(self):
        self.id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        self.contents = Column(String)
        self.answers = relationship("QuestionAnswer", back_populates="question", lazy="dynamic")
        self.correct_answer_id = Column(String, ForeignKey("question_answers.id"))
        self.correct_answer = relationship("QuestionAnswer")
