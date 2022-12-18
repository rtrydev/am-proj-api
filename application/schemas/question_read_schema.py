import marshmallow


class QuestionReadSchema(marshmallow.Schema):
    id = marshmallow.fields.String()
    contents = marshmallow.fields.String()
    answers = marshmallow.fields.List(marshmallow.fields.Dict)
