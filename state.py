import json

from utils import json_serializer


class State(object):
    def __init__(self, map=None, max_turns=23):
        self.map = map
        self.max_turns = max_turns
        self.current_turn = 0

    @property
    def json(self):
        """ Turn object into JSON for storage. """
        return json.dumps({
            'map': self.map,
            'current_turn': self.current_turn,
            'max_turns': self.max_turns,
        }, default=json_serializer)

    def load_from_json(self, json_data):
        """ Load attributes from JSON storage. """
        data = json.loads(json_data)
        print('State data loading: {}'.format(data))
        for key, value in data.items():
            setattr(self, key, value)

