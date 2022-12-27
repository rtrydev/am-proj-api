from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from application.extensions.database import Base
from application.utils.uuid_generator import generate_uuid

from infrastructure.models.waypoint import Waypoint
from infrastructure.models.user import User
from infrastructure.models.question import Question


class WaypointEvent(Base):
    __tablename__ = "waypoint_events"

    id = Column(String, primary_key=True, default=generate_uuid)
    timestamp = Column(Integer)
    waypoint_id = Column(String, ForeignKey("waypoints.id"))
    waypoint = relationship("Waypoint")
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User")
    question_id = Column(String, ForeignKey("questions.id"))
    question = relationship("Question")
    answer_correct = Column(Boolean)
    state = Column(Integer)
