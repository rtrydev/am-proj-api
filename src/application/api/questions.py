import dataclasses
import json

from flask import Response
from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject

from src.application.decorators.auth_decorator import auth
from src.application.schemas.question_read_schema import QuestionReadSchema
from src.application.schemas.question_write_schema import QuestionWriteSchema
from src.domain.enums.roles import Roles
from src.domain.repositories.question_repository import QuestionRepository

questions = Blueprint('question_routes', __name__, url_prefix='/questions')


@questions.route("/")
class Waypoints(MethodView):
    @inject
    def __init__(self, questions_repository: QuestionRepository):
        self.questions_repository = questions_repository

    @questions.response(200, QuestionReadSchema(many=True))
    @auth(Roles.Admin)
    def get(self):
        return self.questions_repository.get_all()

    @questions.arguments(QuestionWriteSchema)
    @questions.response(201)
    @questions.response(403)
    @auth(Roles.Admin)
    def post(self, question):
        result = self.questions_repository.add(question)

        if result is None:
            return Response(status=403)

        return Response(status=201)


@questions.route("/<question_id>")
class WaypointsById(MethodView):
    @inject
    def __init__(self, questions_repository: QuestionRepository):
        self.questions_repository = questions_repository

    @questions.response(200, QuestionReadSchema)
    @questions.response(404)
    def get(self, question_id):
        result = self.questions_repository.get_by_id(question_id)

        if result is None:
            return Response(status=404)

        question = {
            "id": result.id,
            "answers": [dataclasses.asdict(answer) for answer in result.answers],
            "contents": result.contents
        }

        return Response(json.dumps(question), status=200, mimetype="application/json")

    @questions.arguments(QuestionWriteSchema)
    @questions.response(200)
    @questions.response(404)
    @auth(Roles.Admin)
    def put(self, question, question_id):
        result = self.questions_repository.update(question, question_id)

        if result is None:
            return Response(status=404)

        return Response(status=200)

    @questions.response(202)
    @auth(Roles.Admin)
    def delete(self, question_id):
        self.questions_repository.delete(question_id)

        return Response(status=202)
