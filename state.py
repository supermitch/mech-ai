import json
import random

from utils import json_serializer


class State(object):
    def __init__(self, map=None, max_turns=23):
        self.map = map
        self.max_turns = max_turns
        self.current_turn = 0
        self.positions = []  # (x, y) tuple for each player

    @property
    def json(self):
        """ Turn object into JSON for storage. """
        return json.dumps({
            'map': self.map,
            'current_turn': self.current_turn,
            'max_turns': self.max_turns,
            'positions': self.positions,
        }, default=json_serializer)

    def load_from_json(self, json_data):
        """ Load attributes from JSON storage. """
        data = json.loads(json_data)
        for key, value in data.items():
            setattr(self, key, value)

    def set_start_positions(self, player_count):
        """
        Given a map and number of players, set initial player positions.
        """
        possible_positions = []
        rows = self.map.split()
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if cell == '@':
                    possible_positions.append((i, j))
        self.positions = random.sample(possible_positions, player_count)

