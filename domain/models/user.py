from dataclasses import dataclass
from domain.enums.roles import Roles


@dataclass
class User:
    id: str
    username: str
    password: str
    role: Roles
