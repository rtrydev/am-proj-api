import os
import jwt

from domain.services.auth_service import AuthService


class JwtService(AuthService):
    def generate_token(self, payload: dict):
        encoded_jwt = jwt.encode(payload, os.environ['JWT_SECRET'], algorithm="HS256")

        return encoded_jwt
