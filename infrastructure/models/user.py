from sqlalchemy import Column, String, LargeBinary, Integer
from sqlalchemy.orm import relationship

from application.extensions.database import Base
from application.utils.uuid_generator import generate_uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String)
    password = Column(LargeBinary)
    role = Column(Integer)
    question_answers = relationship("QuestionAnswer", back_populates="user", lazy="dynamic")

