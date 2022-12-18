import marshmallow


class UserCredentialsSchema(marshmallow.Schema):
    username = marshmallow.fields.String()
    password = marshmallow.fields.String()
