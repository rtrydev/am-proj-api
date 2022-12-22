from abc import ABC, abstractmethod


class WaypointEventServiceInterface(ABC):
    @abstractmethod
    def init_waypoint_event(self, waypoint_id, user_id):
        pass

    @abstractmethod
    def get_random_question_for_event(self, event_id, user_id):
        pass

    @abstractmethod
    def finish_event(self, event_id, user_id):
        pass

    @abstractmethod
    def validate_event_question(self, event_id, question_id, user_id):
        pass

    @abstractmethod
    def get_events_for_user(self, user_id):
        pass
