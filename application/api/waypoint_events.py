import dataclasses
import json

import jwt
from flask import request, Response
from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject

from application.decorators.auth_decorator import auth
from application.schemas.question_read_schema import QuestionReadSchema
from application.schemas.waypoint_data import WaypointDataSchema
from domain.enums.roles import Roles
from domain.services.waypoint_event_service import WaypointEventServiceInterface

waypoint_events = Blueprint('waypoint_events_routes', __name__, url_prefix='/waypoint_events')


@waypoint_events.route("/")
class WaypointEvents(MethodView):
    @inject
    def __init__(self, waypoint_event_service: WaypointEventServiceInterface):
        self.waypoint_event_service = waypoint_event_service

    @waypoint_events.response(200, WaypointDataSchema(many=True))
    @waypoint_events.response(401)
    @auth(Roles.User)
    def get(self):
        token = request.headers.get('Authorization').replace("Bearer ", "")
        claims = dict(jwt.decode(token, options={"verify_signature": False}))
        user_id = claims.get("id")

        if user_id is None:
            return []

        result = self.waypoint_event_service.get_events_for_user(user_id)

        return Response(json.dumps(result), status=200, mimetype="application/json")

    @waypoint_events.arguments(WaypointDataSchema)
    @waypoint_events.response(200)
    @waypoint_events.response(400)
    @waypoint_events.response(401)
    @waypoint_events.response(403)
    @auth(Roles.User)
    def post(self, waypoint_data):
        waypoint_id = waypoint_data.get("waypoint_id")

        if waypoint_id is None:
            return Response(status=400)

        token = request.headers.get('Authorization').replace("Bearer ", "")
        claims = dict(jwt.decode(token, options={"verify_signature": False}))
        user_id = claims.get("id")

        result = self.waypoint_event_service.init_waypoint_event(waypoint_id, user_id)

        if result is None:
            return Response(status=403)

        json_result = json.dumps({
            "event_id": result.id,
            "timestamp": result.timestamp
        })

        return Response(json_result, 200, mimetype="application/json")


@waypoint_events.route("/<waypoint_event_id>/question")
class WaypointEventsQuestion(MethodView):
    @inject
    def __init__(self, waypoint_event_service: WaypointEventServiceInterface):
        self.waypoint_event_service = waypoint_event_service

    @waypoint_events.response(200, QuestionReadSchema)
    @waypoint_events.response(400)
    @waypoint_events.response(401)
    @waypoint_events.response(403)
    @auth(Roles.User)
    def get(self, waypoint_event_id):
        token = request.headers.get('Authorization').replace("Bearer ", "")
        claims = dict(jwt.decode(token, options={"verify_signature": False}))
        user_id = claims.get("id")

        result = self.waypoint_event_service.get_random_question_for_event(waypoint_event_id, user_id)

        if result is None:
            return Response(status=403)

        question = {
            "id": result.id,
            "answers": [dataclasses.asdict(answer) for answer in result.answers],
            "contents": result.contents
        }

        return Response(json.dumps(question), status=200, mimetype="application/json")
