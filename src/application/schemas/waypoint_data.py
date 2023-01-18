import marshmallow

from src.domain.enums.event_states import EventStates


class WaypointDataSchema(marshmallow.Schema):
    id = marshmallow.fields.String(dump_only=True)
    waypoint_id = marshmallow.fields.String()
    status = marshmallow.fields.Enum(EventStates, dump_only=True)
    answer_correct = marshmallow.fields.Boolean(required=False, dump_only=True)

