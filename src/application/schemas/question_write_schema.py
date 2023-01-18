import marshmallow


class QuestionWriteSchema(marshmallow.Schema):
    id = marshmallow.fields.String(dump_only=True)
    contents = marshmallow.fields.String()
    answers = marshmallow.fields.List(marshmallow.fields.Dict)
    correct_answer_id = marshmallow.fields.String()
