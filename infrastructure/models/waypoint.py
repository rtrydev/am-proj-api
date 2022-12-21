import uuid

from sqlalchemy import Column, String, Float

from application.extensions.database import Base


class Waypoint(Base):
    __tablename__ = "waypoints"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    coordinateX = Column(Float(precision=5))
    coordinateY = Column(Float(precision=5))
