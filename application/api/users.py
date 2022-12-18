import datetime
import json

import bcrypt
from flask import Response
from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject

from application.schemas.user_credentials_schema import UserCredentialsSchema
from domain.repositories.users_repository import UsersRepository
from domain.services.auth_service import AuthService

users = Blueprint('user_routes', __name__, url_prefix='/users')


@users.route("/register")
class UsersRegister(MethodView):
    @inject
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    @users.arguments(UserCredentialsSchema)
    @users.response(201)
    @users.response(403)
    def post(self, credentials):
        result = self.users_repository.add(**credentials)

        if result is None:
            return Response(status=403)

        return Response(status=201)


@users.route("/login")
class UsersRegister(MethodView):
    @inject
    def __init__(self, users_repository: UsersRepository, auth_service: AuthService):
        self.users_repository = users_repository
        self.auth_service = auth_service

    @users.arguments(UserCredentialsSchema)
    @users.response(201)
    @users.response(403)
    @users.response(404)
    def post(self, credentials: UserCredentialsSchema):
        user = self.users_repository.get_by_name(credentials["username"])

        if user is None:
            return Response(status=404)

        input_pass_bytes = credentials["password"].encode("utf-8")
        is_correct_pass = bcrypt.checkpw(input_pass_bytes, user.password)

        if not is_correct_pass:
            return Response(status=403)

        payload = {
            "id": user.id,
            "role": user.role,
            "exp": datetime.datetime.now() + datetime.timedelta(hours=3)
        }
        token = self.auth_service.generate_token(payload)

        return Response(
            json.dumps({
                "auth_token": token
            }),
            status=200
        )
