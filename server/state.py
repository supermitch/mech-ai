import json
import random

from utils import json_serializer
from player import Player


class State(object):
    def __init__(self, map=None, rounds=23, players=None):
        self.map = map
        self.max_turns = rounds
        self.current_turn = 0
        if players:
            self.players = {name: Player(name) for name in players}
            self.set_start_positions()
        else:
            self.players = {}  # List of Player() objects

    @property
    def jsonable(self):
        return {
            'map': self.map,
            'current_turn': self.current_turn,
            'max_turns': self.max_turns,
            'players': {player.name: player.json for player in self.players.values()},
        }

    @property
    def json(self):
        """ Turn object into JSON for storage. """
        return json.dumps(self.jsonable, default=json_serializer)

    def load_from_json(self, json_data):
        """ Load attributes from JSON storage. """
        data = json.loads(json_data)
        for key, value in data.items():
            if key == 'players':
                # Load objects from their own json representation
                players = {}
                for key, value in value.items():
                    player = Player()
                    player.load_from_json(value)
                    players[key] = player
                setattr(self, 'players', players)
            else:
                # Simple load
                setattr(self, key, value)

    def set_start_positions(self):
        """
        Given a map and number of players, set initial player positions.
        """
        possible_positions = []
        rows = self.map.split()
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if cell == '@':
                    possible_positions.append((i, j))
        random.shuffle(possible_positions)
        for player, coords in zip(self.players.values(), possible_positions):
            player.position = coords

