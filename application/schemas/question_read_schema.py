import marshmallow

from application.schemas.answer_schema import AnswerSchema


class QuestionReadSchema(marshmallow.Schema):
    id = marshmallow.fields.String()
    contents = marshmallow.fields.String()
    answers = marshmallow.fields.List(marshmallow.fields.Nested(AnswerSchema(), dump_only=True))
