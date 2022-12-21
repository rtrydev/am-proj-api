import uuid

from sqlalchemy import Column, String, LargeBinary, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from application.extensions.database import Base


class User(Base):
    __tablename__ = "users"

    def __init__(self):
        self.id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        self.username = Column(String)
        self.password = Column(LargeBinary)
        self.role = Column(Integer)
        self.question_answers = relationship("QuestionAnswer", back_populates="user", lazy="dynamic")
