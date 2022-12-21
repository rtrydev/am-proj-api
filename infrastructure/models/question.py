import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from application.extensions.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    contents = Column(String)
    answers = relationship("Answer", back_populates="question", lazy="dynamic")
    correct_answer_id = Column(String)
