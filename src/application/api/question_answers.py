import jwt
from flask import request, Response
from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject

from src.application.decorators.auth_decorator import auth
from src.application.schemas.question_answer_schema import QuestionAnswerSchema
from src.domain.enums.roles import Roles
from src.domain.repositories.question_answers_repository import QuestionAnswersRepository
from src.domain.services.waypoint_event_service import WaypointEventServiceInterface

question_answers = Blueprint('question_answers_routes', __name__, url_prefix='/question_answers')


@question_answers.route("/")
class QuestionAnswers(MethodView):
    @inject
    def __init__(self,
                 question_answers_repository: QuestionAnswersRepository,
                 waypoint_events_service: WaypointEventServiceInterface,
                 ):
        self.question_answers_repository = question_answers_repository
        self.waypoint_events_service = waypoint_events_service

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

        event_id = question_answer.get("event_id")
        question_id = question_answer.get("question_id")
        answer_id = question_answer.get("answer_id")

        is_valid = self.waypoint_events_service.validate_event_question(
            event_id,
            question_id,
            user_id
        )

        if not is_valid:
            return Response(status=403)

        result = self.question_answers_repository.add(
            question_id,
            answer_id,
            user_id
        )

        if result is None:
            return Response(status=403)

        self.waypoint_events_service.finish_event(event_id, user_id, answer_id)

        return Response(status=201)

