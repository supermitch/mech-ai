import json

from utils import json_serializer


class Player(object):

    def __init__(self, name=None):
        self.name = name if name else ''
        self.pos = (0, 0)
        self.health = 0
        self.score = 0
        self.ammo = 0
        self.orientation = 'north'

    @property
    def json(self):
        """ Turn object into JSON for storage. """
        return json.dumps({
            'name': self.name,
            'pos': self.pos,
            'health': self.health,
            'score': self.score,
            'ammo': self.ammo,
            'orientation': self.orientation,
        }, default=json_serializer)

    def load_from_json(self, json_data):
        """ Load attributes from JSON storage. """
        data = json.loads(json_data)
        for key, value in data.items():
            setattr(self, key, value)

    def rotate(self, direction):
        """ Rotates either clockwise or counter clockwise to a new direction. """
        orientations = ['north', 'east', 'south', 'west']
        index = orientations.index(self.orientation)
        index += 1 if direction == 'cw' else -1
        index = index % len(orienations)
        self.orientation = orientations[index]
