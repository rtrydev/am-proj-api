from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.application.extensions.database import Base
from src.application.utils.uuid_generator import generate_uuid


class Answer(Base):
    __tablename__ = "answers"

    id = Column(String, primary_key=True, default=generate_uuid)
    text = Column(String)
    question_id = Column(String, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")
