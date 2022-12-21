import dataclasses
import json

import jwt
from flask import request, Response
from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject

from application.decorators.auth_decorator import auth
from application.schemas.question_answer_schema import QuestionAnswerSchema
from domain.enums.roles import Roles
from domain.repositories.question_answers_repository import QuestionAnswersRepository

question_answers = Blueprint('question_answers_routes', __name__, url_prefix='/question_answers')


@question_answers.route("/")
class QuestionAnswers(MethodView):
    @inject
    def __init__(self, question_answers_repository: QuestionAnswersRepository):
        self.question_answers_repository = question_answers_repository

    @question_answers.response(200, QuestionAnswerSchema(many=True))
    @question_answers.response(401)
    @question_answers.response(403)
    @auth(Roles.User)
    def get(self):
        token = request.headers.get('Authorization').replace("Bearer ", "")
        claims = dict(jwt.decode(token, options={"verify_signature": False}))
        user_id = claims.get("id")

        if user_id is None:
            return Response(status=403)

        result = self.question_answers_repository.get_answers_for_user(user_id)

        schema_result = QuestionAnswerSchema(many=True).dumps(result)

        return Response(schema_result, status=200, mimetype="application/json")

    @question_answers.arguments(QuestionAnswerSchema)
    @question_answers.response(201)
    @question_answers.response(401)
    @question_answers.response(403)
    @auth(Roles.User)
    def post(self, question_answer: QuestionAnswerSchema):
        token = request.headers.get('Authorization').replace("Bearer ", "")
        claims = dict(jwt.decode(token, options={"verify_signature": False}))
        user_id = claims.get("id")

        if user_id is None:
            return Response(status=403)

        result = self.question_answers_repository.add(
            question_answer.get("question_id"),
            question_answer.get("answer_id"),
            user_id
        )

        if result is None:
            return Response(status=403)

        return Response(status=201)

