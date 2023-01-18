from src.application.api.question_answers import question_answers
from src.application.api.questions import questions
from src.application.api.users import users
from src.application.api.waypoint_events import waypoint_events
from src.application.api.waypoints import waypoints


def register_routes(app):
    app.register_blueprint(waypoints)
    app.register_blueprint(users)
    app.register_blueprint(questions)
    app.register_blueprint(question_answers)
    app.register_blueprint(waypoint_events)
