import uuid

from sqlalchemy import Column, String, LargeBinary, Integer
from sqlalchemy.orm import relationship

from application.extensions.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    username = Column(String)
    password = Column(LargeBinary)
    role = Column(Integer)
    question_answers = relationship("QuestionAnswer", back_populates="user", lazy="dynamic")

