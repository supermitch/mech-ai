import datetime

import map_loader


class Game(object):
    def __init__(self, name=name, players=players, map=None):
        """ Initialize a new game. """

        self.name = name,
        self.players = players,  # List of player usernames
        self.status = 'Waiting',
        self.raw_state = self.generate_clean_state(),  # JSON object
        self.created = datetime.datetime.now(),

        map = 'default' if map is None else map
        self.map = map.read_map_file(map)

    def generate_clean_state(self):
        """ Generates a blank game state JSON object. """
        return '{}'

    def load_from_state(self):
        """ Load game attributes from raw game state. """
        pass

    def serialize(self):
        """ Turn game into a serialized game state for storage. """
        pass

    def update(self):
        """ Execute a round. """
        pass

