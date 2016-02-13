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
        rows = state.map.split()[::-1]  # Y-axis is positive, so start at the bottom
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

    def is_valid_coord(self, x, y):
        """ Check if a coordinate is within map bounds. """
        if x < 0 or x > len(self.tiles) or y < 0 or y > len(self.tiles[0]):
            return False
        else:
            return True

    def check_collisions(self, new_x, new_y):
        """ Ensure that move is valid. """

        if not self.is_valid_coord(new_x, new_y):  # Off the map
            return False

        if not self.tiles[new_x][new_y].walkable:  # Not walkable
            return False

        for enemy in self.mechs:  # Check enemy mech collisions
            if enemy.pos == (new_x, new_y):  # Occupied
                return False

        return True

    def update(self, move):
        """ Update our world with the new move. """
        move = move.lower()
        logging.debug('World updating move: <{}>'.format(move))

        if move in ('wait',):
            return True, 'Move ok'

        if move in ('rotate cw', 'rotate ccw'):
            direction = move.split()[1]
            self.player.rotate(direction)
            return True, 'Move ok'

        if move in ('shoot',):
            if self.player.ammo > 0:  # Don't go below zero
                self.player.ammo -= 1
            else:
                return False, 'No ammo'
            direction = self.player.orientation
            movement = {
                'north': (0, 1),
                'east': (1, 0),
                'south': (0, -1),
                'west': (-1, 0),
            }.get(direction.lower())
            shot = self.player.pos  # start position
            while self.is_valid_coord(*shot):
                shot[0] += movement[0]
                shot[1] += movement[1]
                if self.check_collisions(shot[0], shot[1]):
                    for enemy in self.mechs:  # Check enemy mech collisions
                        if enemy.pos == (shot[0], shot[1]):  # Occupied
                            enemy.health -= 1
                            self.player.score += 1
                    break  # Stops at walls, but no points
            return True, 'Move ok'

        movement = {
            'go north': (0, 1),
            'go east': (1, 0),
            'go south': (0, -1),
            'go west': (-1, 0),
        }.get(move, None)

        if movement is None:
            return False, 'Unknown move <{}>'.format(move)

        new_x = self.player.pos[0] + movement[0]
        new_y = self.player.pos[1] + movement[1]
        if self.check_collisions(new_x, new_y):
            self.player.pos = new_x, new_y
            return True, 'Move ok'
        else:
            return False, 'Failed collision check'

