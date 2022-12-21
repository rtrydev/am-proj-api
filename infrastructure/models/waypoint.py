import uuid

from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID

from application.extensions.database import Base


class Waypoint(Base):
    __tablename__ = "waypoints"

    def __init__(self):
        self.id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        self.title = Column(String)
        self.description = Column(String)
        self.coordinateX = Column(Float(precision=5))
        self.coordinateY = Column(Float(precision=5))
