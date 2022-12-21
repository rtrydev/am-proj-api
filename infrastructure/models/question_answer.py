import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from application.extensions.database import Base


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    def __init__(self):
        self.id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        self.question_id = Column(String, ForeignKey("questions.id"))
        self.question = relationship("Question", back_populates="answers")
        self.user_id = Column(String, ForeignKey("users.id"))
        self.user = relationship("User", back_populates="question_answers")
        self.text = Column(String)
