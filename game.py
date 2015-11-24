import map


class Game(object):
    def __init__(self, players, map_name='default'):
        """ Initialize a new game. """
        self.players = players  # List of player usernames
        self.map = map.read_map_file(map_name)

    def load_from_state(self):
        """ Load game attributes from raw game state. """
        pass

    def serialize(self):
        """ Turn game into a serialized game state for storage. """
        pass

    def update(self):
        """ Execute a round. """
        pass

