import marshmallow


class QuestionAnswerSchema(marshmallow.Schema):
    id = marshmallow.fields.String(dump_only=True)
    answer_id: marshmallow.fields.String()
    question_id: marshmallow.fields.String()
    text: marshmallow.fields.String()
