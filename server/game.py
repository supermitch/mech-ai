import datetime
import json

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
        self.status = GAME_STATUS.lobby
        self.created = datetime.datetime.now()

        # These attributes are persisted in the state, not DB properties
        map = map_loader.read_map_file(self.map_name)
        self.state = state.State(map=map, rounds=rounds, players=players)

        self.queue = queue.Queue(players=players)

    def update(self, username, move):
        """ Execute a round. """

        tiles = world.World(self)  # Convert our self (a game object) into a World

        print('Updating move: {}'.format(move))
        move = move.lower()
        player = self.state.players[username]


        movement = {
            'go north': (0, 1),
            'go east': (1, 0),
            'go south': (0, -1),
            'go west': (-1, 0),
        }.get(move, None)

        if movement is not None:
            # TODO: Check collisions!
            player.position[0] += movement[0]
            player.position[1] += movement[1]

        self.queue.increment_move()
        self.state.current_turn += 1
        if self.state.current_turn == self.state.max_turns:
            self.status = GAME_STATUS.complete
        return True

