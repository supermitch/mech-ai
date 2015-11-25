import datetime
import json

import map_loader


class GAME_STATUS(object):
    """ Game status constants. """
    lobby = 'waiting for players'
    waiting = 'waiting for moves'
    playing = 'playing'
    cancelled = 'cancelled'
    complete = 'complete'


class Game(object):
    def __init__(self, name=name, players=players, map='default'):
        """ Initialize a new game. """
        self.name = name,
        self.players = players,  # List of player usernames
        self.status = GAME_STATUS.lobby,
        self.created = datetime.datetime.now(),

        # These attributes are persisted in the raw_state, not DB properties
        self.map = map.read_map_file(map)
        self.current_turn = 0
        self.max_turns = 0

        self.raw_state = self.serialize(),  # JSON state (a DB property)

    def load_state_from_json(self):
        """ Load game attributes from raw game state. """
        state = json.loads(self.raw_state)
        self.map = state['map']
        self.current_turn, self.max_turns = state['turn']

    def serialize_state(self):
        """ Turn game state into a serialized game state for storage. """
        state = {
            'map': self.map,
            'turn': [self.current_turn, self.max_turns],
        }
        return json.dumps(state)

    def update(self):
        """ Execute a round. """
        self.current_turn += 1
        if self.current_turn == self.max_turns:
            self.status = GAME_STATUS.complete

