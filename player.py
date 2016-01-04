import json

from utils import json_serializer


class Player(object):

    def __init__(self):
        self.name = ''
        self.position = (0, 0)
        self.health = 0
        self.score = 0
        self.ammo = 0

    @property
    def json(self):
        """ Turn object into JSON for storage. """
        return json.dumps({
            'name': self.name,
            'position': self.position,
            'health': self.health,
            'score': self.score,
            'ammo': self.ammo,
        }, default=json_serializer)

    def load_from_json(self, json_data):
        """ Load attributes from JSON storage. """
        data = json.loads(json_data)
        for key, value in data.items():
            setattr(self, key, value)
