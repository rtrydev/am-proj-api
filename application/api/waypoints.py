import dataclasses
import json

from flask import Response
from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject

from application.decorators.auth_decorator import auth
from domain.enums.roles import Roles
from domain.repositories.waypoint_repository import WaypointRepository
from application.schemas.waypoint_schema import WaypointSchema

waypoints = Blueprint('waypoint_routes', __name__, url_prefix='/waypoints')


@waypoints.route("/")
class Waypoints(MethodView):
    @inject
    def __init__(self, waypoints_repository: WaypointRepository):
        self.waypoints_repository = waypoints_repository

    @waypoints.response(200, WaypointSchema(many=True))
    def get(self):
        return self.waypoints_repository.get_all()

    @waypoints.arguments(WaypointSchema)
    @waypoints.response(201)
    @waypoints.response(403)
    @auth(Roles.Admin)
    def post(self, waypoint):
        result = self.waypoints_repository.add(waypoint)

        if result is None:
            return Response(status=403)

        return Response(status=201)


@waypoints.route("/<waypoint_id>")
class WaypointsById(MethodView):
    @inject
    def __init__(self, waypoints_repository: WaypointRepository):
        self.waypoints_repository = waypoints_repository

    @waypoints.response(200, WaypointSchema)
    @waypoints.response(404)
    def get(self, waypoint_id):
        result = self.waypoints_repository.get_by_id(waypoint_id)

        if result is None:
            return Response(status=404)

        result_json = json.dumps(dataclasses.asdict(result))

        return Response(result_json, status=200, mimetype="application/json")

    @waypoints.arguments(WaypointSchema)
    @waypoints.response(200)
    @waypoints.response(404)
    def put(self, waypoint, waypoint_id):
        result = self.waypoints_repository.update(waypoint, waypoint_id)

        if result is None:
            return Response(status=404)

        return Response(status=200)

    @waypoints.response(202)
    def delete(self, waypoint_id):
        self.waypoints_repository.delete(waypoint_id)

        return Response(status=202)
