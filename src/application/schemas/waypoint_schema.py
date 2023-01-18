import marshmallow


class WaypointSchema(marshmallow.Schema):
    id = marshmallow.fields.String(dump_only=True)
    title = marshmallow.fields.String()
    description = marshmallow.fields.String()
    coordinateX = marshmallow.fields.Number()
    coordinateY = marshmallow.fields.Number()
