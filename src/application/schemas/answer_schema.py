import marshmallow


class AnswerSchema(marshmallow.Schema):
    id = marshmallow.fields.String()
    text = marshmallow.fields.String(dump_only=True)
