import marshmallow


class QuestionAnswerSchema(marshmallow.Schema):
    id = marshmallow.fields.String()
    question_id = marshmallow.fields.String()
    answer_id = marshmallow.fields.String()
