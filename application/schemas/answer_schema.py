import marshmallow


class AnswerSchema(marshmallow.Schema):
    answer_id = marshmallow.fields.String()
    text = marshmallow.fields.String(dump_only=True)
