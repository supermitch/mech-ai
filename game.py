import datetime
import json

import map_loader


class GAME_STATUS(object):
    """ Game status constants. """
    lobby = 'lobby'  # In matchmaking lobby, waiting for all players
    playing = 'playing'  # In game mode, waiting for turns
    complete = 'complete'  # Game finished
    cancelled = 'cancelled'  # Broken?


class PLAYER_STATUS(object):
    waiting = 'waiting'  # Hasn't joined the lobby yet
    playing = 'playing'  # Sending moves and waiting for game state
    lost = 'lost'  # Missed turns/broken?


class Queue(object):
    """ An object essentially describing whose turn it is. """
    def __init__(self, players):
        self.current_move = 0
        self.last_move = None
        self.statuses = {player: 'waiting' for player in players}
        self.time_stamps = {player: None for player in players}

    @property
    def is_complete(self):
        """ Return True if all players present. """
        return all(status in ('joined', 'playing') for status in self.statuses.values())

    def set_status(self, player, status):
        """ Set new status and update time stamp. """
        self.statuses[player] = status
        self.time_stamps[player] = datetime.datetime.now()

    @property
    def json(self):
        """ Turn game queue into JSON for storage. """
        data = {
            'current_move': self.current_move,
            'last_move': self.last_move,
            'statuses': self.statuses,
            'time_stamps': self.time_stamps,
        }
        return json.dumps(data)


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

        self.state = self.serialize_state()
        self.queue = Queue(players)

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


