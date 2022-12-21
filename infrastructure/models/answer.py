import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from application.extensions.database import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    text = Column(String)
    question_id = Column(String, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")
