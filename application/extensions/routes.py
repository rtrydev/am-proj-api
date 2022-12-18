from application.api.questions import questions
from application.api.users import users
from application.api.waypoints import waypoints


def register_routes(app):
    app.register_blueprint(waypoints)
    app.register_blueprint(users)
    app.register_blueprint(questions)
