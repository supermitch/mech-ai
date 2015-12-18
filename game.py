import datetime
import json

import map_loader
import queue
import state
import utils


class GAME_STATUS(object):
    """ Game status constants. """
    lobby = 'lobby'  # In matchmaking lobby, waiting for all players
    playing = 'playing'  # In game mode, waiting for turns
    complete = 'complete'  # Game finished
    cancelled = 'cancelled'  # Broken?


class PLAYER_STATUS(object):
    waiting = 'waiting'  # Hasn't joined the lobby yet
    joined = 'joined'  # Has joined the lobby
    playing = 'playing'  # Sending moves and waiting for game state
    lost = 'lost'  # Missed turns/broken?


class Game(object):
    def __init__(self, players=None, name=None, map_name='default'):
        """
        Initialize a new game.

        Note that when we load a game from the repo, we init an empty
        game, so all our arguments to the constructor are optional.
        """
        self.name = name
        self.map_name = map_name
        self.players = players  # List of player usernames
        self.status = GAME_STATUS.lobby
        self.created = datetime.datetime.now()

        # These attributes are persisted in the raw_state, not DB properties
        self.map = map_loader.read_map_file(map_name)
        print(self.map)
        self.current_turn = 0
        self.max_turns = 0

        self.state = self.serialize_state()
        self.queue = queue.Queue(players=players)

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
        self.queue = queue.Queue()
        print('Model.queue {}'.format(model.queue))
        self.queue.load_from_json(model.queue)

    def update(self):
        """ Execute a round. """
        self.current_turn += 1
        if self.current_turn == self.max_turns:
            self.status = GAME_STATUS.complete

