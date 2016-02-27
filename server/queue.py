import datetime
import logging
import json

import utils


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

    def increment_move(self):
        """ Increment the index of the current move. """
        self.current_move = (self.current_move + 1) % len(self.move_order)

    def is_turn(self, player):
        """ Return if it this player's turn or not. """
        return player == self.move_order[self.current_move]

    @property
    def current_turn(self):
        """ Return username of current player. """
        return self.move_order[self.current_move]

    def set_status(self, player, status):
        """ Set new status and update time stamp. """
        self.statuses[player] = status
        self.time_stamps[player] = datetime.datetime.now()
        logging.debug('Statuses: {}'.format(self.statuses))

    @property
    def json(self):
        """ Turn game queue into JSON for storage. """
        return json.dumps({
            'current_move': self.current_move,
            'last_move': self.last_move,
            'move_order': self.move_order,
            'statuses': self.statuses,
            'time_stamps': self.time_stamps,
        }, default=utils.json_serializer)

    def load_from_json(self, data):
        """ Load attributes from JSON storage. """
        attrs = ['current_move', 'last_move', 'move_order', 'statuses', 'time_stamps']
        queue_data = json.loads(data)
        for attr in attrs:
            setattr(self, attr, queue_data.get(attr))


