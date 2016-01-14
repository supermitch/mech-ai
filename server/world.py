from tile import Tile


class World(object):

    def __init__(self, game):
        print(game.state)
        self.generate_tiles(game.state)

    def generate_tiles(self, state):
        """ Generate a tileset from the game state. """
        print('Map:\n' + state.map)
        map = state.map
        rows = map.split()
        height = len(rows)
        width = len(rows[0])
        tiles = [[None for _ in range(height)] for _ in range(width)]
        print('Tiles:\n{}'.format(tiles))
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                tiles[x][y] = Tile(char, x, y)
        print('Tiles:\n{}'.format(tiles))
