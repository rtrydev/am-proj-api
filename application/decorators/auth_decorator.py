import functools
import os
import jwt
from flask import request, Response
from jwt import DecodeError, ExpiredSignatureError

from domain.enums.roles import Roles


def auth(required_role: Roles):
    def _auth_decorator(func):
        @functools.wraps(func)
        def decorated_function(*args, **kwargs):
            bearer_token = request.headers.get('Authorization')
            token = bearer_token.replace("Bearer ", "") if bearer_token else None

            if token is None:
                return Response(status=401)

            try:
                result = jwt.decode(token, os.environ['JWT_SECRET'], ["HS256"])
            except DecodeError:
                return Response(status=401)
            except ExpiredSignatureError:
                return Response(status=401)

            claim_role = result.get('role')

            if claim_role is None:
                return Response(status=403)

            if claim_role < required_role:
                return Response(status=403)

            return func(*args, **kwargs)
        return decorated_function
    return _auth_decorator
