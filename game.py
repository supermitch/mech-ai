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
    def __init__(self, id=None, players=None, name=None, map_name='default', max_turns=17):
        """
        Initialize a new game.

        Note that when we load a game from the repo, we init an empty
        game, so all our arguments to the constructor are optional.
        """
        self.id = id
        self.name = name
        self.map_name = map_name
        self.players = players  # List of player usernames
        self.status = GAME_STATUS.lobby
        self.created = datetime.datetime.now()

        # These attributes are persisted in the state, not DB properties
        map = map_loader.read_map_file(map_name)
        print(map)

        self.state = state.State(map=map, max_turns=max_turns)
        self.queue = queue.Queue(players=players)


    def update(self):
        """ Execute a round. """
        self.current_turn += 1
        if self.current_turn == self.max_turns:
            self.status = GAME_STATUS.complete

