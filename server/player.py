import json

from utils import json_serializer


class Player(object):

    def __init__(self, name=None):
        self.name = name if name else ''
        self.pos = (0, 0)
        self.health = 10
        self.score = 0
        self.ammo = 10
        self.orientation = 'north'

    @property
    def jsonable(self):
        """ Turn object into JSON repr. """
        return {
            'name': self.name,
            'pos': self.pos,
            'health': self.health,
            'score': self.score,
            'ammo': self.ammo,
            'orientation': self.orientation,
        }

    @property
    def json(self):
        """ Turn object into JSON for storage. """
        return json.dumps(self.jsonable, default=json_serializer)

    def load_from_json(self, json_data):
        """ Load attributes from JSON storage. """
        self.load_from_data(json.loads(json_data))

    def load_from_data(self, data):
        """ Load attribs from a dictionary. """
        for key, value in data.items():
            setattr(self, key, value)

    def rotate(self, direction):
        """ Rotates either clockwise or counter clockwise to a new direction. """
        dirs = ['north', 'east', 'south', 'west']
        index = dirs.index(self.orientation)
        index += 1 if direction == 'cw' else -1
        index = index % len(dirs)
        self.orientation = dirs[index]
