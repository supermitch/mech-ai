import datetime
import json
import logging

import map_loader
import queue
import state
import utils
import world


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
    def __init__(self, id=None, players=None, name='Mech AI', map_name='default', rounds=17):
        """
        Initialize a new game.

        Note that when we load a game from the repo, we init an empty
        game, so all our arguments to the constructor are optional.
        """
        self.id = id
        self.name = name if name else 'Mech AI'
        self.map_name = map_name if map_name else 'default'
        self.players = players  # List of player usernames
        self.winner = None
        self.status = GAME_STATUS.lobby
        self.created = datetime.datetime.now()

        # These attributes are persisted in the state, not DB properties
        map = map_loader.read_map_file(self.map_name)
        self.state = state.State(map=map, rounds=rounds, players=players)

        self.queue = queue.Queue(players=players)
        self.transactions = []

    def update(self, username, move):
        """ Execute a round. """
        the_world = world.World(self)  # Convert our self (a game object) into a World
        success, reason = the_world.update(move)

        if success:
            self.queue.increment_move()
            self.state.increment_turn()
            if self.state.game_complete:
                self.status = GAME_STATUS.complete

        return success, reason

