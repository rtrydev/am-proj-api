from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from application.extensions.database import Base
from application.utils.uuid_generator import generate_uuid


class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, default=generate_uuid)
    contents = Column(String)
    answers = relationship("Answer", back_populates="question", lazy="dynamic")
    correct_answer_id = Column(String)
