from tile import Tile


class World(object):

    def __init__(self, game):
        print(game.state)
        self.generate_tiles(game.state)

    def generate_tiles(self, state):
        """ Generate a tileset from the game state. """
        print(state.map)

