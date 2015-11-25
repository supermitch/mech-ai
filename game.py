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
    def __init__(self, name=name, players=players, map_name='default'):
        """ Initialize a new game. """
        self.name = name,
        self.map_name = map_name
        self.players = players,  # List of player usernames
        self.status = GAME_STATUS.lobby,
        self.created = datetime.datetime.now(),

        # These attributes are persisted in the raw_state, not DB properties
        self.map = map.read_map_file(map_name)
        self.current_turn = 0
        self.max_turns = 0

        self.state = self.serialize(),  # JSON state (a DB property)

    def load_state_from_json(self):
        """ Load game attributes from raw game state. """
        state = json.loads(self.state)
        self.map = state['map']
        self.current_turn, self.max_turns = state['turn']

    def serialize_state(self):
        """ Turn game state into a serialized game state for storage. """
        state = {
            'map': self.map,
            'turn': [self.current_turn, self.max_turns],
        }
        return json.dumps(state)

    def load_from_model(self, model):
        """ Populate a Game from an NDB game model. """
        attrs = ['name', 'players', 'status', 'created', 'map_name', 'state']
        for attr in attrs:
            setattr(self, attr, getattr(model, attr))

        self.load_state_from_json()

    def update(self):
        """ Execute a round. """
        self.current_turn += 1
        if self.current_turn == self.max_turns:
            self.status = GAME_STATUS.complete


