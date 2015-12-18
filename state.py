from utils import json_serializer


class State(object):
    def __init__(self):
        self.map = map
        self.current_turn
        self.max_turns

    @property
    def json(self):
        """ Turn game state into JSON for storage. """
        return json.dumps({
            'map': self.current_move,
            'current_move': self.last_move,
            'max_turns': self.move_order,
        }, default=json_serializer)

    def load_from_json(self, json_data):
        """ Load attributes from JSON storage. """
        data = json.loads(json_data)
        for key, value in data.items():
            setattr(self, key, value)

