import logging

from tile import Tile
from mech import Mech, Enemy, Player


class World(object):

    def __init__(self, game):
        print(game.state)
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
        """ Generate enemy mechs from the game state. """
        self.mechs = []
        logging.debug('Generating enemy mechs...')
        for name, player in game.state.players.items():
            print(name, player, game.state.json)
            if game.queue.is_turn(name):
                self.player = Player(player.name, player.pos, player.health, player.score, player.ammo)
            else:
                self.mechs.append(Enemy(player.name, player.pos, player.health, player.score, player.ammo))


