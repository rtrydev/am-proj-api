import marshmallow
from domain.enums.roles import Roles


class UserReadSchema(marshmallow.Schema):
    id = marshmallow.fields.String()
    username = marshmallow.fields.String()
    role = marshmallow.fields.Enum(Roles)
