from sqlalchemy import Column, String, Float

from application.extensions.database import Base
from application.utils.uuid_generator import generate_uuid


class Waypoint(Base):
    __tablename__ = "waypoints"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String)
    description = Column(String)
    coordinateX = Column(Float(precision=5))
    coordinateY = Column(Float(precision=5))
