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
    joined = 'joined'  # Has joined the lobby
    playing = 'playing'  # Sending moves and waiting for game state
    lost = 'lost'  # Missed turns/broken?


class Queue(object):
    """ An object essentially describing whose turn it is. """
    def __init__(self, players=None):
        """
        Note that we may init an empty Queue, if we are loading from the repo.
        """
        self.current_move = 0
        self.last_move = None
        if players is None:
            self.move_order = []
            self.statuses = {}
            self.time_stamps = {}
        else:
            self.move_order = [player for player in players]
            self.statuses = {player: 'waiting' for player in players}
            self.time_stamps = {player: None for player in players}

    @property
    def is_complete(self):
        """ Return True if all players present. """
        return all(status in ('joined', 'playing') for status in self.statuses.values())

    @property
    def not_joined(self):
        """ Return a list of players we're waiting on. """
        return [player for player, status in self.statuses.items() if status == 'waiting']

    def is_turn(self, player):
        """ Return if it this player's turn or not. """
        return player == self.move_order[self.current_move]

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
            'move_order': self.move_order,
            'statuses': self.statuses,
            'time_stamps': self.time_stamps,
        }
        return json.dumps(data)

    def load_from_json(self, data):
        """ Load attributes from JSON storage. """
        attrs = ['current_move', 'last_move', 'move_order', 'statuses', 'time_stamps']
        queue_data = json.loads(data)
        for attr in attrs:
            setattr(self, attr, queue_data.get(attr))


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
        self.queue = Queue(players=players)

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
        new_queue = Queue()
        new_queue.load_from_json(model.queue)
        self.queue = new_queue

    def update(self):
        """ Execute a round. """
        self.current_turn += 1
        if self.current_turn == self.max_turns:
            self.status = GAME_STATUS.complete


