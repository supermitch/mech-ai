import logging

from tile import Tile


class World(object):
    """ A world is an Object representing our game state. """

    def __init__(self, game):
        """ Generate our world given our game object. """
        self.generate_tiles(game.state)
        self.generate_mechs(game)

    def generate_tiles(self, state):
        """ Generate a tileset from the game state. """
        logging.debug('Generating tiles...')
        map = state.map
        rows = map.split()
        height = len(rows)
        width = len(rows[0])
        self.tiles = [[None for _ in range(height)] for _ in range(width)]
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                self.tiles[x][y] = Tile(char, x, y)

    def generate_mechs(self, game):
        """ Generate mechs from the game state. """
        self.mechs = []
        for name, player in game.state.players.items():
            if game.queue.is_turn(name):
                logging.debug('{} is player'.format(name))
                self.player = player
            else:
                logging.debug('{} is mech'.format(name))
                self.mechs.append(player)

    def update(self, move):
        """ Update our world with the new move. """
        move = move.lower()
        logging.debug('World updating move: <{}>'.format(move))

        movement = {
            'go north': (0, 1),
            'go east': (1, 0),
            'go south': (0, -1),
            'go west': (-1, 0),
        }.get(move, None)

        if movement is None:
            return False, 'Unknown move <{}>'.format(move)

        if self.check_collisions(movement):
            self.player.pos[0] += movement[0]
            self.player.pos[1] += movement[1]
        else:
            return False, 'Failed collision check'

        return True, 'Move ok'

    def check_collisions(self, movement):
        """ Ensure that move is valid. """
        new_x = self.player.pos[0] + movement[0]
        new_y = self.player.pos[1] + movement[1]

        if new_x < 0 or new_y < 0:
            return False  # Off the map
        try:  # Check unwalkable tile collisions
            if not self.tiles[new_x][new_y].walkable:
                return False
        except IndexError:  # Off the map
            return False

        for enemy in self.mechs:  # Check enemy mech collisions
            if enemy.pos == (new_x, new_y):  # Occupied
                return False

        return True
