from dataclasses import dataclass


@dataclass
class Waypoint:
    id: str
    title: str
    description: str
    coordinateX: float
    coordinateY: float
